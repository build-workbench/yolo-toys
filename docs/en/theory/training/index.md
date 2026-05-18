---
title: Training Background
---

# Training Background

Understanding what happens before inference helps you make better decisions about model selection, fine-tuning, and deployment.

## Why pre-training matters

The models in YOLO-Toys share a common pattern:

1. **Pre-training**: Learn general features from large datasets
2. **Fine-tuning**: Adapt to specific tasks/domains
3. **Inference**: Deploy for real-world use

The pre-training phase determines:
- **Generalization**: How well the model handles novel inputs
- **Feature quality**: How rich the learned representations are
- **Transferability**: How easily the model adapts to new domains

## Articles in this section

### [Loss Functions](/en/theory/training/loss-functions)

Understanding the mathematical objectives that shape model behavior:
- YOLO family losses (CIoU, VFL, DFL)
- DETR bipartite matching
- Contrastive losses for vision-language models

## Pre-training data scale

| Model | Pre-training Data | Scale |
|-------|------------------|-------|
| YOLOv8 | COCO + Objects365 | ~2M images |
| DETR | COCO | 118K images |
| OWL-ViT | LAION-400M | 400M image-text pairs |
| BLIP | LAION + CC3M | ~130M image-text pairs |

## What to read next

- [Loss Functions](/en/theory/training/loss-functions) for detailed loss explanations
- [Model Matrix](/en/reference/models) for practical specifications
