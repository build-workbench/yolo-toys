---
title: Detection Paradigms Comparison
---

# Detection Paradigms: A Systematic Comparison

This chapter provides a unified comparison of the three major detection paradigms: anchor-based, anchor-free, and transformer-based approaches.

## Historical context

```
2014 ────────────────────────────────────────────────────── 2024

Anchor-based                    Anchor-free              Transformer
────────────                    ───────────              ───────────

Faster R-CNN (2015)             CenterNet (2019)         DETR (2020)
     │                              │                        │
SSD (2016)                      FCOS (2019)             Deformable DETR
     │                              │                        │
YOLOv2-v5 (2017-2020)           YOLOv8 (2023)           DINO (2022)
     │                              │                        │
RetinaNet (2017)                RTMDet (2022)           Co-DETR (2023)

     └──────────────────────────────┴────────────────────────┘
                              Today's landscape
```

## Anchor-based detection

### Core idea

Place predefined anchor boxes at each spatial location, predict offsets:

$$
\begin{aligned}
b_x &= a_x + a_w \cdot t_x \\
b_y &= a_y + a_h \cdot t_y \\
b_w &= a_w \cdot e^{t_w} \\
b_h &= a_h \cdot e^{t_h}
\end{aligned}
$$

Where $(a_x, a_y, a_w, a_h)$ is the anchor and $(t_x, t_y, t_w, t_h)$ are predicted offsets.

### Anchor design

Anchors are typically designed using:

1. **Manual design**: Based on dataset statistics (e.g., COCO anchors)
2. **K-means clustering**: Learn anchors from ground truth boxes
3. **Genetic evolution**: Optimize anchors for mAP

### Representative models

| Model | Year | Key Innovation |
|-------|------|----------------|
| Faster R-CNN | 2015 | RPN for region proposals |
| SSD | 2016 | Multi-scale feature maps |
| YOLOv2 | 2017 | Anchor boxes + BN |
| RetinaNet | 2017 | Focal loss for class imbalance |
| YOLOv3 | 2018 | FPN for multi-scale |
| YOLOv4 | 2020 | CSP + PANet |
| YOLOv5 | 2020 | Auto-anchor learning |

### Limitations

1. **Hyperparameter sensitivity**: Anchor design significantly affects performance
2. **Aspect ratio mismatch**: Fixed anchors may not fit unusual objects
3. **Duplicate predictions**: Requires NMS post-processing
4. **Dense scene struggles**: Overlapping objects cause confusion

## Anchor-free detection

### Core idea

Predict object centers directly, then regress size from center features:

$$
\begin{aligned}
\text{Center:} \quad & (c_x, c_y) = \text{heatmap peak} \\
\text{Size:} \quad & (w, h) = \text{regression from center features}
\end{aligned}
$$

### Approaches

1. **Center-based** (CenterNet): Predict center heatmap, regress size
2. **Point-based** (FCOS): Predict per-point classification and regression
3. **Keypoint-based**: Detect corners or extreme points

### Representative models

| Model | Year | Key Innovation |
|-------|------|----------------|
| CornerNet | 2018 | Detect corner pairs |
| CenterNet | 2019 | Center heatmap |
| FCOS | 2019 | Per-pixel prediction |
| YOLOX | 2021 | Anchor-free YOLO |
| YOLOv8 | 2023 | Decoupled head + DFL |

### Advantages

1. **No anchor design**: One fewer hyperparameter set
2. **Better generalization**: Adapts to unusual aspect ratios
3. **Fewer duplicates**: Natural suppression through heatmap peaks

### Challenges

1. **Training stability**: Center prediction is harder to optimize
2. **Feature alignment**: Center features must capture object extent
3. **Small objects**: Heatmap resolution limits small object detection

## Transformer-based detection

### Core idea

Learn object queries that attend to image features:

$$
\text{Query}_i \xrightarrow{\text{cross-attention}} \text{Image features} \xrightarrow{\text{FFN}} (\text{class}_i, \text{box}_i)
$$

### Key components

1. **Object queries**: Learned embeddings that specialize in detecting objects
2. **Transformer encoder**: Process image features with self-attention
3. **Transformer decoder**: Queries attend to encoded features
4. **Bipartite matching**: Hungarian matching for loss computation

### Representative models

| Model | Year | Key Innovation |
|-------|------|----------------|
| DETR | 2020 | End-to-end set prediction |
| Deformable DETR | 2021 | Sparse attention for convergence |
| DINO | 2022 | Contrastive denoising |
| Co-DETR | 2023 | Collaborative training |

### Advantages

1. **No NMS**: Set prediction handles duplicates
2. **No anchors**: Learned queries replace hand-designed boxes
3. **Global context**: Attention sees entire image
4. **Clean architecture**: Easy to understand and extend

### Challenges

1. **Slow convergence**: 500 epochs for full training
2. **Small objects**: Struggles with small object detection
3. **Computational cost**: Quadratic attention complexity

## Quantitative comparison

### COCO val2017 mAP

| Model | Paradigm | mAP | FPS (V100) | Params |
|-------|----------|-----|------------|--------|
| YOLOv5l | Anchor-based | 49.0 | 50 | 46.5M |
| YOLOv8l | Anchor-free | 52.9 | 30 | 43.7M |
| DETR-R101 | Transformer | 43.5 | 10 | 60M |
| DINO-R50 | Transformer | 50.4 | 12 | 47M |

### Speed vs accuracy trade-off

```
mAP
 │
 │                                    ★ YOLOv8l
 │                              ★ YOLOv8m
 │                         ★ YOLOv8s
 │                    ★ YOLOv8n
 │
 │                         ◆ DINO
 │                    ◆ DETR
 │
 └────────────────────────────────────────── FPS
      10    20    30    40    50    60    70
```

## When to choose which paradigm

### Anchor-based (YOLOv5)

- You need maximum inference speed
- Your objects have consistent aspect ratios
- You want mature tooling and documentation

### Anchor-free (YOLOv8)

- Your objects have varied aspect ratios
- You want fewer hyperparameters
- You're starting a new project (recommended default)

### Transformer (DETR)

- You're detecting large, well-separated objects
- You need global context reasoning
- You're doing research on detection

## References

1. Ren, S., et al. "Faster R-CNN: Towards Real-Time Object Detection." NeurIPS 2015.
2. Law, H., Deng, J. "CornerNet: Detecting Objects as Paired Keypoints." ECCV 2018.
3. Carion, N., et al. "End-to-End Object Detection with Transformers." ECCV 2020.

---

## What to read next

- [YOLO Family Evolution](/en/theory/detection/yolo-family) for detailed YOLO history
- [DETR Architecture](/en/theory/detection/detr-transformer) for transformer details
- [Model Matrix](/en/reference/models) for practical selection
