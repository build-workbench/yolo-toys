---
title: Model Matrix
---

# Model Matrix

Complete specifications for all supported model families. Use this reference to select the right model for your task, understand the performance trade-offs, and configure inference parameters correctly.

<div class="yt-callout yt-callout--insight">
  <div class="yt-callout__label">Selection principle</div>
  <div class="yt-callout__body">YOLOv8 for throughput-critical applications; DETR for dense or complex scenes; OWL-ViT / Grounding DINO for open-vocabulary tasks; BLIP for language-grounded understanding.</div>
</div>

## Quick comparison

| Family | Paradigm | GPU Warm Latency | COCO mAP | Open-vocab | Notes |
|--------|----------|-----------------|----------|------------|-------|
| YOLOv8n | Anchor-free | 4ms | 37.3 | No | Best throughput |
| YOLOv8s | Anchor-free | 6ms | 44.9 | No | Balanced |
| YOLOv8m | Anchor-free | 12ms | 50.2 | No | High accuracy |
| YOLOv8l | Anchor-free | 18ms | 52.9 | No | Maximum accuracy |
| DETR (ResNet-50) | Transformer | 90ms | ~42 | No | Dense scenes |
| OWL-ViT (base-patch32) | VLM | 110ms | — | Yes | Novel classes |
| Grounding DINO | VLM | 130ms | — | Yes | Phrase grounding |
| BLIP-Caption | VLM | 70ms | — | Yes | Image captioning |
| BLIP-VQA | VLM | 70ms | — | Yes | Visual QA |

---

## YOLO family

YOLO-Toys serves the YOLOv8 family via the `YOLOHandler`. Model files must be in Ultralytics `.pt` format. The handler automatically infers the task type (detection, segmentation, or pose) from the model weights.

### Detection models

```bash
yolov8n.pt   # Nano   — 6.2M params, fastest
yolov8s.pt   # Small  — 11.2M params, balanced
yolov8m.pt   # Medium — 25.9M params, higher accuracy
yolov8l.pt   # Large  — 43.7M params, maximum accuracy
yolov8x.pt   # XLarge — 68.2M params, research-grade
```

| Model | Parameters | Disk size | COCO mAP (val2017) | GPU warm (p50) |
|-------|-----------|----------|--------------------|---------------|
| yolov8n | 3.2M | 6.2 MB | 37.3 | 4ms |
| yolov8s | 11.2M | 21.5 MB | 44.9 | 6ms |
| yolov8m | 25.9M | 49.7 MB | 50.2 | 12ms |
| yolov8l | 43.7M | 83.7 MB | 52.9 | 18ms |

Trained on COCO 2017, 80 classes: person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush.

### Segmentation models

```bash
yolov8n-seg.pt   # Nano segmentation
yolov8s-seg.pt   # Small segmentation
yolov8m-seg.pt   # Medium segmentation
```

Returns: bounding boxes + pixel-level segmentation masks. The `task` field in the response is `"segment"`.

### Pose models

```bash
yolov8n-pose.pt   # Nano pose
yolov8s-pose.pt   # Small pose
```

Returns: bounding boxes + 17 COCO keypoints (nose, left/right eye, left/right ear, left/right shoulder, left/right elbow, left/right wrist, left/right hip, left/right knee, left/right ankle). The `task` field is `"pose"`.

### Default inference parameters

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| `conf` | 0.25 | [0.0, 1.0] | Minimum confidence threshold |
| `iou` | 0.45 | [0.0, 1.0] | NMS IoU threshold |
| `max_det` | 300 | [1, 1000] | Maximum detections per image |
| `imgsz` | model default | int | Input image size override |
| `half` | false | bool | FP16 inference (CUDA only) |

---

## HuggingFace models

These models are loaded from the HuggingFace Hub on first use. Loading requires network access and takes 2–10 seconds on first request. Subsequent requests use the warm cached model.

### DETR — Detection Transformer

```bash
facebook/detr-resnet-50         # Standard DETR, ResNet-50 backbone
facebook/detr-resnet-101        # DETR with ResNet-101 backbone (higher accuracy)
facebook/detr-resnet-50-panoptic  # Panoptic segmentation variant
```

DETR uses transformer encoder-decoder with learned object queries. No anchors, no NMS. Particularly strong on dense scenes and unusual aspect ratios. Slow to converge during training but clean inference semantics.

| Property | Value |
|----------|-------|
| Handler | `DETRHandler` |
| Category | `ModelCategory.HF_DETR` |
| GPU warm latency | ~90ms |
| CPU warm latency | ~380ms |
| Input preprocessing | PIL image, ImageProcessor normalization |

```json
{ "conf": 0.5, "max_det": 100 }
```

### OWL-ViT — Open-Vocabulary Detection

```bash
google/owlvit-base-patch32      # Base model, patch size 32
google/owlvit-large-patch14     # Large model, patch size 14 (higher accuracy)
```

Text-conditioned detection using contrastive pre-training. Provide `text_queries` in your request to detect custom object categories without retraining.

| Property | Value |
|----------|-------|
| Handler | `OWLViTHandler` |
| Category | `ModelCategory.HF_OWLVIT` |
| GPU warm latency | ~110ms |
| Required parameter | `text_queries: ["a cat", "a dog"]` |

### Grounding DINO — Phrase Grounding

```bash
IDEA-Research/grounding-dino-tiny    # Tiny variant
IDEA-Research/grounding-dino-base    # Base variant
```

Open-set detection with natural language phrase grounding. More expressive than OWL-ViT for complex descriptions.

| Property | Value |
|----------|-------|
| Handler | `GroundingDINOHandler` |
| Category | `ModelCategory.HF_GROUNDING` |
| GPU warm latency | ~130ms |
| Required parameter | `text_queries: ["person wearing a red jacket"]` |

### BLIP — Image Captioning and VQA

```bash
Salesforce/blip-image-captioning-base    # Image captioning
Salesforce/blip-image-captioning-large   # Larger captioning model
Salesforce/blip-vqa-base                 # Visual question answering
```

Unified vision-language model supporting both generation (captioning) and understanding (VQA). Route determines behavior: `/caption` uses `BLIPCaptionHandler`, `/vqa` uses `BLIPVQAHandler`.

| Property | Value |
|----------|-------|
| Caption handler | `BLIPCaptionHandler` |
| VQA handler | `BLIPVQAHandler` |
| GPU warm latency | ~70ms |
| VQA parameter | `question: "What is in the image?"` |

---

## Model ID inference rules

YOLO-Toys infers the correct handler from the model ID through a cascading resolution strategy:

1. **Exact registry match**: if the model ID appears in `MODEL_REGISTRY`, use the registered category
2. **File extension heuristic**: `.pt` files → `ModelCategory.YOLO_*` (with `seg`/`pose` sub-variants from filename)
3. **Keyword matching**: `detr` → `HF_DETR`, `owlvit` → `HF_OWLVIT`, `blip-image-captioning` → `HF_BLIP_CAPTION`, `blip-vqa` → `HF_BLIP_VQA`, `grounding` or `dino` → `HF_GROUNDING`
4. **HuggingFace path fallback**: any ID containing `/` not matched above → `HF_DETR`

This means common models work without explicit registration. Novel architectures require extending `ModelCategory` and `_CATEGORY_HANDLER_MAP`.

---

## What to read next

- [Handler Topology](/en/architecture/handlers) — how models map to handler implementations
- [Request Lifecycle](/en/architecture/request-flow) — the full inference path
- [Performance Benchmarks](/en/reference/benchmarks) — latency and throughput data
- [REST API](/en/api/rest-api) — endpoint documentation
- [Configuration Reference](/en/reference/configuration-reference) — cache and runtime settings
