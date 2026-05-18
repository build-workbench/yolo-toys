---
title: Detection Algorithms
---

# Detection Algorithms Overview

Object detection is the foundational task for YOLO-Toys. This section covers the three major paradigms: anchor-based, anchor-free, and transformer-based detection.

## The detection problem

Given an image, object detection requires:

1. **Localization**: Where are the objects? (bounding boxes)
2. **Classification**: What are the objects? (class labels)

The challenge is that the number of objects varies per image, and objects can appear at any location and scale.

## Three paradigms

### Anchor-based detection

The dominant paradigm from 2014–2022:

1. Place anchor boxes (priors) at each spatial location
2. Predict offsets from anchors
3. Apply NMS to remove duplicates

**Representatives**: YOLOv2–v5, Faster R-CNN, SSD, RetinaNet

**Pros**:
- Well-understood optimization landscape
- Good performance with proper anchor design

**Cons**:
- Anchor design is hyperparameter-sensitive
- Many duplicate predictions
- Struggles with unusual aspect ratios

### Anchor-free detection

Treat detection as keypoint estimation:

1. Predict object centers directly
2. Regress size from center features
3. No anchor boxes needed

**Representatives**: YOLOv8, CenterNet, FCOS

**Pros**:
- No anchor hyperparameters
- Fewer duplicate predictions
- Better generalization to unusual objects

**Cons**:
- Newer, less mature
- Training can be less stable

### Transformer-based detection

Treat detection as set prediction:

1. Learn object queries
2. Queries attend to image features
3. Direct set output, no NMS

**Representatives**: DETR, Deformable DETR

**Pros**:
- End-to-end, no hand-designed components
- Clean architecture
- Good for research

**Cons**:
- Slow convergence
- Struggles with small objects
- Higher computational cost

## Paradigm comparison

| Feature | Anchor-based | Anchor-free | Transformer |
|---------|--------------|-------------|-------------|
| NMS needed | Yes | Yes/No | No |
| Anchors | Yes | No | No |
| Training stability | High | Medium | Low |
| Inference speed | Fast | Fast | Slower |
| Small objects | Good | Medium | Struggles |
| Large objects | Good | Good | Excellent |

## Model selection guide

```
[Task requirements?]
│
├─ Real-time edge? ──────▶ YOLOv8n (anchor-free, fastest)
│
├─ Production API? ──────▶ YOLOv8s/m (anchor-free, balanced)
│
├─ Maximum accuracy? ────▶ YOLOv8l/x or DETR
│
├─ Dense scenes? ────────▶ DETR (handles overlap well)
│
├─ Novel classes? ───────▶ OWL-ViT (open-vocabulary)
│
└─ Text-conditioned? ────▶ OWL-ViT or Grounding DINO
```

## What to read next

- [YOLO Family Evolution](/en/theory/detection/yolo-family) for anchor-based/anchor-free history
- [DETR Architecture](/en/theory/detection/detr-transformer) for transformer-based detection
- [Model Matrix](/en/reference/models) for concrete specifications
