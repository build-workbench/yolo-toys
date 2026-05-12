# 支持的模型参考

所有支持模型的完整列表和规格。

---

## 📊 模型对比

### 检测模型

| 模型 | 大小 | 速度 (GPU) | mAP | 适用场景 |
|-------|------|-------------|-----|----------|
| YOLOv8n | 6.2M | ~5ms | 37.3 | 实时、边缘设备 |
| YOLOv8s | 11.2M | ~6ms | 44.9 | 平衡 |
| YOLOv8m | 25.9M | ~8ms | 50.2 | 更高精度 |
| YOLOv8l | 43.7M | ~12ms | 52.9 | 最大精度 |

### 多模态模型

| 模型 | 任务 | 速度 (GPU) |
|-------|------|-------------|
| BLIP-Caption | 图像描述 | ~120ms |
| BLIP-VQA | 视觉问答 | ~95ms |

---

## 🏷️ YOLO 模型

### YOLOv8 检测

```bash
MODEL_NAME=yolov8n.pt  # Nano - 最快
MODEL_NAME=yolov8s.pt  # Small - 平衡
MODEL_NAME=yolov8m.pt  # Medium - 准确
```

**COCO 类别 (80):** person, bicycle, car, motorcycle, airplane, bus, train, truck, boat 等。

### YOLOv8 分割

```bash
MODEL_NAME=yolov8n-seg.pt
```

### YOLOv8 姿态

```bash
MODEL_NAME=yolov8n-pose.pt
```

---

## 🤗 HuggingFace 模型

### DETR (Detection Transformer)

```bash
MODEL_NAME=facebook/detr-resnet-50
```

### OWL-ViT (Open Vocabulary)

```bash
MODEL_NAME=google/owlvit-base-patch32
```

配合 `text_queries` 参数用于零样本检测。

### BLIP (图像描述)

```bash
MODEL_NAME=Salesforce/blip-image-captioning-base
```

---

## ⚙️ 模型配置

### 默认参数

| 模型类型 | conf | iou | max_det |
|------------|------|-----|---------|
| YOLO Detection | 0.25 | 0.45 | 300 |
| DETR | 0.50 | - | 100 |

---

## 🔗 相关文档

- [Handler 模式](../architecture/handlers) — 模型实现方式
- [REST API](../api/rest-api) — API 用法
