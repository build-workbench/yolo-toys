---
title: Loss Functions
---

# Detection Loss Functions

Understanding loss functions is essential for diagnosing model behavior and tuning inference parameters. This chapter covers the key losses used by the model families in YOLO-Toys.

## Why losses matter at inference time

Even though losses are not directly used during inference, they shape model behavior:

1. **Confidence calibration**: Classification losses affect score reliability
2. **Box quality**: Regression losses determine localization accuracy
3. **Threshold tuning**: Understanding losses helps set confidence and IoU thresholds

## YOLO family losses

### YOLOv1: Sum-squared error

YOLOv1 uses a simple sum-squared error loss:

$$
\mathcal{L} = \lambda_{coord} \mathcal{L}_{box} + \mathcal{L}_{conf} + \lambda_{noobj} \mathcal{L}_{noobj} + \mathcal{L}_{cls}
$$

The loss treats all errors equally, which leads to poor localization for large objects.

### YOLOv3–v5: Binary cross-entropy + CIoU

$$
\mathcal{L}_{cls} = -\sum_{c} [y_c \log(\hat{y}_c) + (1-y_c) \log(1-\hat{y}_c)]
$$

$$
\mathcal{L}_{box} = 1 - CIoU
$$

Where CIoU considers overlap area, distance between centers, and aspect ratio:

$$
CIoU = IoU - \frac{\rho^2(b, b^{gt})}{c^2} - \alpha v
$$

### YOLOv8: VFL + DFL + CIoU

YOLOv8 uses three combined losses:

1. **VFL (Varifocal Loss)**: Asymmetric focal loss for classification
2. **DFL (Distribution Focal Loss)**: Box regression as distribution prediction
3. **CIoU Loss**: Complete IoU for box overlap

```python
# VFL: Addresses class imbalance
vfl(q, p) = -q * log(p) if q > 0 else -α * q * log(1-p)

# DFL: Continuous distribution over discrete bins
# Instead of predicting x directly, predict P(x|age)
dfl(y, ŷ) = -∑_{j=y_l}^{y_r} P(age_j) * log(ŷ(age_j))
```

## DETR losses

### Bipartite matching loss

DETR uses Hungarian matching to find the optimal assignment:

$$
\hat{\sigma} = \arg\min_{\sigma \in \mathfrak{S}_N} \sum_i^N \mathcal{L}_{match}(y_i, \hat{y}_{\sigma(i)})
$$

### Hungarian loss

After matching, the final loss combines:

$$
\mathcal{L}_{Hungarian} = \lambda_{cls} \mathcal{L}_{cls} + \lambda_{L1} \mathcal{L}_{L1} + \lambda_{giou} \mathcal{L}_{giou}
$$

## Contrastive losses (OWL-ViT, Grounding DINO)

### InfoNCE loss

Used in contrastive pre-training:

$$
\mathcal{L} = -\frac{1}{N} \sum_i \log \frac{\exp(\text{sim}(I_i, T_i) / \tau)}{\sum_{j=1}^N \exp(\text{sim}(I_i, T_j) / \tau)}
$$

Where $\tau$ is a learned temperature and $\text{sim}$ is cosine similarity.

## Cross-entropy losses (BLIP)

### Autoregressive captioning loss

$$
\mathcal{L}_{cap} = -\sum_{t=1}^T \log P(w_t | w_{<t}, I)
$$

Where $w_t$ is the token at position $t$ and $I$ is the image.

## Loss comparison summary

| Model | Classification | Regression | Matching |
|-------|---------------|------------|----------|
| YOLOv5 | BCE | CIoU | Anchor-based |
| YOLOv8 | VFL | DFL + CIoU | Anchor-free |
| DETR | CE | L1 + GIoU | Hungarian |
| OWL-ViT | BCE | L1 | Contrastive |
| BLIP | CE | — | Autoregressive |

## References

1. Lin, T., et al. "Focal Loss for Dense Object Detection." ICCV 2017.
2. Zheng, Z., et al. "Distance-IoU Loss: Faster and Better Learning." AAAI 2020.
3. Li, J., et al. "BLIP: Bootstrapping Language-Image Pre-training." ICML 2023.

---

## What to read next

- [YOLO Family Evolution](/en/theory/detection/yolo-family) for loss function evolution
- [Model Matrix](/en/reference/models) for practical specifications
