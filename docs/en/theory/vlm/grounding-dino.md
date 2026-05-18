---
title: Grounding DINO
---

# Grounding DINO: Phrase Grounding Meets Detection

Grounding DINO combines the best of grounding models and detection models: it can detect objects described by natural language phrases with high accuracy, while maintaining the ability to work with open vocabulary.

## The grounding problem

**Phrase grounding**: Given an image and a text description, find the image regions corresponding to each phrase.

Example:
```
Text: "A dog chasing a red ball in the park"
Phrases: ["dog", "red ball", "park"]
Output: [box_dog, box_ball, box_park]
```

This is more precise than open-vocabulary detection because it leverages the full sentence context.

## Architecture

Grounding DINO is a fusion of:

1. **DINO**: A detection model with self-supervised pre-training
2. **Grounding**: Text-conditioned localization

```
┌─────────────────────────────────────────────────────────────┐
│                   Grounding DINO                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Image ────▶ Backbone ────▶ Image Features                  │
│                                │                            │
│                                │                            │
│  Text ─────▶ BERT ──────────▶ Text Features                 │
│                                │                            │
│                                ▼                            │
│                    Feature Fusion (cross-attn)               │
│                                │                            │
│                                ▼                            │
│                    Detection Head                            │
│                                │                            │
│                                ▼                            │
│                    Grounded Boxes                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Key innovations

### 1. Feature fusion

Early fusion of image and text features:

```python
# Cross-modal attention
fused = cross_attention(image_feat, text_feat)
# Use fused features for detection
```

### 2. Contrastive phrase grounding

Train with contrastive loss to align phrases with regions:

$$
\mathcal{L}_{ground} = -\log \frac{\exp(\text{sim}(r_i, p_i))}{\sum_j \exp(\text{sim}(r_i, p_j))}
$$

### 3. Zero-shot transfer

Pre-trained on large image-text datasets, transfers to new domains without fine-tuning.

## Performance

| Model | COCO mAP | LVIS APr | RefCOCO Acc |
|-------|----------|----------|-------------|
| OWL-ViT | 42.6 | 31.5 | - |
| GLIP | 49.8 | 27.0 | - |
| Grounding DINO | **52.5** | **33.8** | 85.6 |

## When to use Grounding DINO

::: tip Recommended
- Detailed scene descriptions with multiple objects
- Phrase-level grounding (not just object names)
- High accuracy open-vocabulary detection
:::

::: warning Note
Slower than YOLOv8 for detection-only tasks. Use OWL-ViT for simple open-vocab detection.
:::

## References

1. Liu, S., et al. "Grounding DINO: Marrying DINO with Grounded Pre-Training." ECCV 2024. [arXiv:2303.05499](https://arxiv.org/abs/2303.05499)

---

## What to read next

- [OWL-ViT](/en/theory/vlm/owl-vit) for comparison
- [BLIP](/en/theory/vlm/blip) for image captioning
