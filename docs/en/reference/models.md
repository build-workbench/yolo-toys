# Supported Models Reference

Complete list of all supported models with specifications.

---

## 📊 Model Comparison

### Detection Models

| Model | Size | Speed (GPU) | mAP | Best For |
|-------|------|-------------|-----|----------|
| YOLOv8n | 6.2M | ~5ms | 37.3 | Real-time, edge devices |
| YOLOv8s | 11.2M | ~6ms | 44.9 | Balanced |
| YOLOv8m | 25.9M | ~8ms | 50.2 | Higher accuracy |
| YOLOv8l | 43.7M | ~12ms | 52.9 | Maximum accuracy |

### Multimodal Models

| Model | Task | Speed (GPU) |
|-------|------|-------------|
| BLIP-Caption | Image Captioning | ~120ms |
| BLIP-VQA | Visual QA | ~95ms |

---

## 🏷️ YOLO Models

### YOLOv8 Detection

```bash
MODEL_NAME=yolov8n.pt  # Nano - fastest
MODEL_NAME=yolov8s.pt  # Small - balanced
MODEL_NAME=yolov8m.pt  # Medium - accurate
```

**COCO Classes (80):** person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, etc.

### YOLOv8 Segmentation

```bash
MODEL_NAME=yolov8n-seg.pt
```

### YOLOv8 Pose

```bash
MODEL_NAME=yolov8n-pose.pt
```

---

## 🤗 HuggingFace Models

### DETR (Detection Transformer)

```bash
MODEL_NAME=facebook/detr-resnet-50
```

### OWL-ViT (Open Vocabulary)

```bash
MODEL_NAME=google/owlvit-base-patch32
```

Use with `text_queries` parameter for zero-shot detection.

### BLIP (Image Captioning)

```bash
MODEL_NAME=Salesforce/blip-image-captioning-base
```

---

## ⚙️ Model Configuration

### Default Parameters

| Model Type | conf | iou | max_det |
|------------|------|-----|---------|
| YOLO Detection | 0.25 | 0.45 | 300 |
| DETR | 0.50 | - | 100 |

---

## 🔗 Related Documentation

- [Handler Pattern](../architecture/handlers) — How models are implemented
- [REST API](../api/rest-api) — API usage
