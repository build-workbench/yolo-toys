---
title: Theory and Algorithms
---

# Theory and Algorithms

This chapter provides deep technical background on the vision models served by YOLO-Toys. Understanding these foundations helps you choose the right model, tune inference parameters, and reason about performance trade-offs.

<FigureFrame
  title="Figure 1. Model family landscape"
  caption="YOLO-Toys serves five distinct model families, each with different architectural assumptions, training paradigms, and inference characteristics."
>
  <SvgRenderer src="/images/hero-architecture.svg" alt="Model family landscape" title="Model Families" />
</FigureFrame>

## Chapter structure

### [Detection Algorithms](/en/theory/detection/)

Object detection is the core task for most YOLO-Toys use cases. This section covers:

- **[YOLO Family Evolution](/en/theory/detection/yolo-family)** — From YOLOv1's grid-based prediction to YOLOv8's anchor-free architecture, tracing eight years of single-shot detection innovation
- **[DETR Architecture](/en/theory/detection/detr-transformer)** — How transformers enable end-to-end detection without anchors or NMS
- **[Detection Paradigms](/en/theory/detection/detection-paradigms)** — Comparing anchor-based, anchor-free, and transformer-based approaches

### [Vision-Language Models](/en/theory/vlm/)

Open-vocabulary detection and image understanding models:

- **[OWL-ViT](/en/theory/vlm/owl-vit)** — Text-conditioned detection using contrastive pre-training
- **[Grounding DINO](/en/theory/vlm/grounding-dino)** — Phrase grounding with fused vision-language features
- **[BLIP](/en/theory/vlm/blip)** — Image captioning and visual question answering

### [Training Background](/en/theory/training/)

Understanding what happens before inference:

- **[Loss Functions](/en/theory/training/loss-functions)** — Detection losses, contrastive losses, and their gradients

## Why this matters

YOLO-Toys abstracts away model-family differences, but the abstraction is not free. Understanding the underlying architectures helps you:

1. **Choose the right model** — YOLOv8 excels at throughput; DETR handles dense scenes better; OWL-ViT detects novel classes
2. **Tune parameters intelligently** — Confidence thresholds, IoU thresholds, and NMS settings have different meanings per family
3. **Diagnose failures** — Why did OWL-ViT miss this detection? Why is DETR slower on this image?
4. **Plan extensions** — What would it take to add a new model family?

## Reading paths

::: tip For Operators
Start with [Detection Paradigms](/en/theory/detection/detection-paradigms) for a comparative overview, then dive into the specific family you're deploying.
:::

::: tip For Contributors
Read [YOLO Family Evolution](/en/theory/detection/yolo-family) and [DETR Architecture](/en/theory/detection/detr-transformer) to understand the architectural patterns that YOLO-Toys normalizes.
:::

::: tip For Researchers
The [Vision-Language Models](/en/theory/vlm/) section covers the newest additions to the detection ecosystem. These models represent the frontier of open-vocabulary perception.
:::

## What to read next

- [YOLO Family Evolution](/en/theory/detection/yolo-family) for the canonical detection lineage
- [OWL-ViT](/en/theory/vlm/owl-vit) for open-vocabulary detection
- [Model Selection Guide](/en/reference/models) for practical decision trees
