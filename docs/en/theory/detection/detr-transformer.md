---
title: DETR Architecture
---

# DETR: Detection Transformer

DETR (Detection Transformer) represents a paradigm shift in object detection: it eliminates the need for hand-designed components like anchors and non-maximum suppression (NMS) by framing detection as a direct set prediction problem.

<FigureFrame
  title="Figure 1. DETR architecture"
  caption="DETR uses a CNN backbone for feature extraction, followed by a transformer encoder-decoder. Object queries learn to attend to image regions and directly predict bounding boxes."
>
  <SvgRenderer src="/images/detr-architecture.svg" alt="DETR architecture diagram" title="DETR Architecture" />
</FigureFrame>

## The set prediction insight

Traditional detectors predict a large number of boxes (thousands) and then filter them using NMS. This creates several problems:

1. **Duplicate predictions**: NMS is a heuristic that may remove true positives
2. **Anchor design**: Requires careful tuning of anchor sizes and aspect ratios
3. **Post-processing**: Detection is not truly end-to-end

DETR's insight: **treat detection as a set prediction problem**. The model directly outputs a fixed-size set of predictions, one per "object query", with no post-processing needed.

## Architecture overview

### Backbone (CNN)

DETR uses a standard CNN backbone (ResNet-50 or ResNet-101) to extract features:

```
Input: H × W × 3
         ↓
ResNet backbone
         ↓
Output: H/32 × W/32 × 2048
```

The feature map is then projected to a lower dimension (d = 256) and flattened into a sequence.

### Positional encoding

Since transformers have no built-in notion of spatial position, DETR adds 2D sinusoidal positional encodings to the feature map:

```python
# 2D positional encoding
PE(pos, 2i)   = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))

# Applied separately for x and y dimensions
PE_2d(x, y) = concat(PE(x), PE(y))
```

### Transformer encoder

The encoder processes the flattened feature map with self-attention:

```
┌─────────────────────────────────────────────────────────────┐
│                   Transformer Encoder                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Features + Positional Encoding                             │
│       │                                                     │
│       ▼                                                     │
│  Self-Attention ──── Each position attends to all others    │
│       │                                                     │
│       ▼                                                     │
│  FFN ────────────── Position-wise transformation            │
│       │                                                     │
│       × 6 layers                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Transformer decoder

The decoder takes **object queries** — learned embeddings that will become the final predictions:

```
┌─────────────────────────────────────────────────────────────┐
│                   Transformer Decoder                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Object Queries (N learned vectors)                         │
│       │                                                     │
│       ▼                                                     │
│  Self-Attention ──── Queries attend to each other           │
│       │                                                     │
│       ▼                                                     │
│  Cross-Attention ─── Queries attend to encoder output       │
│       │                                                     │
│       ▼                                                     │
│  FFN                                                        │
│       │                                                     │
│       × 6 layers                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key insight**: Object queries compete for different image regions through cross-attention. Each query learns to specialize in detecting objects at certain positions.

### Prediction heads

Two parallel FFNs produce the final outputs:

- **Class head**: N × (C + 1) class predictions (including "no object")
- **Box head**: N × 4 box coordinates (center_x, center_y, width, height)

## Bipartite matching loss

The core innovation is the loss function. DETR uses **Hungarian matching** to find the optimal assignment between predictions and ground truth:

### Step 1: Hungarian matching

Find the permutation σ that minimizes the matching cost:

$$
\hat{\sigma} = \arg\min_{\sigma} \sum_i^N \mathcal{L}_{match}(y_i, \hat{y}_{\sigma(i)})
$$

Where the matching cost combines classification and box similarity:

<div v-pre>

$$
\mathcal{L}_{match} = -\mathbb{1}_{\{c_i \neq \varnothing\}} \hat{p}_{\sigma(i)}(c_i) + \mathbb{1}_{\{c_i \neq \varnothing\}} \mathcal{L}_{box}(b_i, \hat{b}_{\sigma(i)})
$$

</div>

### Step 2: Loss computation

After matching, compute the final loss:

$$
\mathcal{L} = \sum_i^N \left[ \lambda_{cls} \mathcal{L}_{cls} + \lambda_{box} \mathcal{L}_{box} + \lambda_{giou} \mathcal{L}_{giou} \right]
$$

The box loss uses L1 and GIoU:

$$
\mathcal{L}_{box} = \lambda_{L1} \| b_i - \hat{b}_{\sigma(i)} \|_1 + \lambda_{giou} (1 - GIoU(b_i, \hat{b}_{\sigma(i)}))
$$

## No NMS, no anchors

The bipartite matching loss ensures each ground truth object is matched to exactly one prediction. This eliminates:

1. **Duplicate predictions**: Each query produces at most one box
2. **Anchor tuning**: Object queries are learned, not designed
3. **NMS heuristics**: Set prediction handles duplicates naturally

## Object queries: What do they learn?

Research has shown that object queries learn to specialize in:

- **Spatial regions**: Some queries focus on image center, others on edges
- **Object scales**: Some queries detect large objects, others small
- **Object counts**: Queries learn to "compete" for objects

Visualization of query attention patterns reveals they learn meaningful spatial specializations without explicit supervision.

## Performance

| Model | Backbone | mAP (COCO) | FPS |
|-------|----------|------------|-----|
| DETR | ResNet-50 | 42.0 | 12 |
| DETR | ResNet-101 | 43.5 | 10 |
| DETR-DC5 | ResNet-101 | 47.0 | 8 |

*DC5 = dilated C5 stage for higher resolution features*

### Strengths

- **Large objects**: DETR excels at detecting large objects
- **No hand-designed components**: Fully learned detection
- **Clean architecture**: Easy to understand and extend

### Weaknesses

- **Small objects**: Struggles with small object detection
- **Training time**: Requires 500 epochs for full training
- **Convergence**: Slower convergence than anchor-based methods

## Deformable DETR

An extension that addresses convergence issues by using **deformable attention**:

- Each query only attends to a small set of key sampling points
- Sampling points are learned offsets from reference points
- 10× faster convergence, better small object detection

```python
# Standard attention: O(HW × HW)
# Deformable attention: O(HW × K), K << HW

# Each query attends to K learned sampling points
deform_attn(q, p) = Σ_m W_m Σ_k A_mqk · W'_m · x(p + Δp_mqk)
```

## When to use DETR

::: tip Dense scenes
DETR excels when objects are well-separated and large. Use for scene understanding tasks.
:::

::: tip Research
DETR's clean architecture makes it ideal for research on detection and set prediction.
:::

::: warning Small objects
For small object detection, consider Deformable DETR or YOLOv8 instead.
:::

## References

1. Carion, N., et al. "End-to-End Object Detection with Transformers." ECCV 2020. [arXiv:2005.12872](https://arxiv.org/abs/2005.12872)

2. Zhu, X., et al. "Deformable DETR: Deformable Transformers for End-to-End Object Detection." ICLR 2021. [arXiv:2010.04102](https://arxiv.org/abs/2010.04102)

---

## What to read next

- [Detection Paradigms](/en/theory/detection/detection-paradigms) for comparing DETR with YOLO
- [YOLO Family Evolution](/en/theory/detection/yolo-family) for the anchor-based lineage
- [Model Matrix](/en/reference/models) for practical selection
