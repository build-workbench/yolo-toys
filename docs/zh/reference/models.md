---
title: 模型矩阵
---

# 模型矩阵

所有支持的模型家族完整规格说明。使用本参考文档选择适合任务的模型、理解性能取舍，并正确配置推理参数。

<div class="yt-callout yt-callout--insight">
  <div class="yt-callout__label">选型原则</div>
  <div class="yt-callout__body">吞吐量优先选 YOLOv8；密集或复杂场景选 DETR；开放词汇任务选 OWL-ViT / Grounding DINO；语言驱动的图像理解选 BLIP。</div>
</div>

## 快速对比

| 家族 | 范式 | GPU 热延迟 | COCO mAP | 开放词汇 | 备注 |
|------|------|-----------|----------|---------|------|
| YOLOv8n | 无锚框 | 4ms | 37.3 | 否 | 最高吞吐量 |
| YOLOv8s | 无锚框 | 6ms | 44.9 | 否 | 均衡 |
| YOLOv8m | 无锚框 | 12ms | 50.2 | 否 | 高精度 |
| YOLOv8l | 无锚框 | 18ms | 52.9 | 否 | 最高精度 |
| DETR (ResNet-50) | Transformer | 90ms | ~42 | 否 | 密集场景 |
| OWL-ViT (base-patch32) | VLM | 110ms | — | 是 | 新类别检测 |
| Grounding DINO | VLM | 130ms | — | 是 | 短语定位 |
| BLIP-Caption | VLM | 70ms | — | 是 | 图像描述 |
| BLIP-VQA | VLM | 70ms | — | 是 | 视觉问答 |

---

## YOLO 家族

YOLO-Toys 通过 `YOLOHandler` 提供 YOLOv8 家族服务。模型文件须为 Ultralytics `.pt` 格式。handler 会从模型权重中自动推断任务类型（检测、分割或姿态估计）。

### 检测模型

```bash
yolov8n.pt   # Nano   — 6.2M 参数，最快
yolov8s.pt   # Small  — 11.2M 参数，均衡
yolov8m.pt   # Medium — 25.9M 参数，更高精度
yolov8l.pt   # Large  — 43.7M 参数，最高精度
yolov8x.pt   # XLarge — 68.2M 参数，科研级
```

| 模型 | 参数量 | 磁盘大小 | COCO mAP (val2017) | GPU 热延迟 (p50) |
|------|-------|---------|-------------------|----------------|
| yolov8n | 3.2M | 6.2 MB | 37.3 | 4ms |
| yolov8s | 11.2M | 21.5 MB | 44.9 | 6ms |
| yolov8m | 25.9M | 49.7 MB | 50.2 | 12ms |
| yolov8l | 43.7M | 83.7 MB | 52.9 | 18ms |

训练数据：COCO 2017，80 个类别。

### 分割模型

```bash
yolov8n-seg.pt   # Nano 分割
yolov8s-seg.pt   # Small 分割
yolov8m-seg.pt   # Medium 分割
```

返回：边界框 + 像素级分割掩码。响应中 `task` 字段为 `"segment"`。

### 姿态估计模型

```bash
yolov8n-pose.pt   # Nano 姿态
yolov8s-pose.pt   # Small 姿态
```

返回：边界框 + 17 个 COCO 关键点（鼻子、左/右眼、左/右耳、左/右肩、左/右肘、左/右腕、左/右髋、左/右膝、左/右踝）。响应中 `task` 字段为 `"pose"`。

### 默认推理参数

| 参数 | 默认值 | 范围 | 说明 |
|------|-------|-----|------|
| `conf` | 0.25 | [0.0, 1.0] | 最小置信度阈值 |
| `iou` | 0.45 | [0.0, 1.0] | NMS IoU 阈值 |
| `max_det` | 300 | [1, 1000] | 每图最大检测数 |
| `imgsz` | 模型默认 | int | 输入图像尺寸覆盖 |
| `half` | false | bool | FP16 推理（仅 CUDA） |

---

## HuggingFace 模型

这些模型在首次使用时从 HuggingFace Hub 加载。加载需要网络访问，首次请求耗时 2–10 秒。后续请求使用热缓存模型。

### DETR — 检测 Transformer

```bash
facebook/detr-resnet-50         # 标准 DETR，ResNet-50 骨干
facebook/detr-resnet-101        # DETR + ResNet-101 骨干（更高精度）
facebook/detr-resnet-50-panoptic  # 全景分割变体
```

DETR 使用 Transformer 编码器-解码器与可学习目标查询。无锚框，无 NMS。在密集场景和非常规宽高比上表现特别突出。

| 属性 | 值 |
|------|---|
| Handler | `DETRHandler` |
| Category | `ModelCategory.HF_DETR` |
| GPU 热延迟 | ~90ms |
| CPU 热延迟 | ~380ms |
| 输入预处理 | PIL 图像，ImageProcessor 归一化 |

### OWL-ViT — 开放词汇检测

```bash
google/owlvit-base-patch32      # 基础模型，patch 尺寸 32
google/owlvit-large-patch14     # 大型模型，patch 尺寸 14（更高精度）
```

使用对比预训练实现文本条件检测。在请求中提供 `text_queries` 即可检测任意自定义类别，无需重新训练。

| 属性 | 值 |
|------|---|
| Handler | `OWLViTHandler` |
| Category | `ModelCategory.HF_OWLVIT` |
| GPU 热延迟 | ~110ms |
| 必填参数 | `text_queries: ["一只猫", "一只狗"]` |

### Grounding DINO — 短语定位

```bash
IDEA-Research/grounding-dino-tiny    # Tiny 变体
IDEA-Research/grounding-dino-base    # Base 变体
```

支持自然语言短语定位的开放集检测。对复杂描述的表达能力强于 OWL-ViT。

| 属性 | 值 |
|------|---|
| Handler | `GroundingDINOHandler` |
| Category | `ModelCategory.HF_GROUNDING` |
| GPU 热延迟 | ~130ms |
| 必填参数 | `text_queries: ["穿红色夹克的人"]` |

### BLIP — 图像描述与视觉问答

```bash
Salesforce/blip-image-captioning-base    # 图像描述
Salesforce/blip-image-captioning-large   # 更大的描述模型
Salesforce/blip-vqa-base                 # 视觉问答
```

统一的视觉-语言模型，支持生成（描述）和理解（VQA）两种能力。路由决定行为：`/caption` 使用 `BLIPCaptionHandler`，`/vqa` 使用 `BLIPVQAHandler`。

| 属性 | 值 |
|------|---|
| 描述 handler | `BLIPCaptionHandler` |
| VQA handler | `BLIPVQAHandler` |
| GPU 热延迟 | ~70ms |
| VQA 参数 | `question: "图中有什么？"` |

---

## 模型 ID 推断规则

YOLO-Toys 通过级联解析策略从模型 ID 推断正确的 handler：

1. **精确注册表匹配**：若模型 ID 在 `MODEL_REGISTRY` 中，使用已注册的类别
2. **文件扩展名启发式**：`.pt` 文件 → `ModelCategory.YOLO_*`（从文件名中识别 `seg`/`pose` 子变体）
3. **关键词匹配**：`detr` → `HF_DETR`、`owlvit` → `HF_OWLVIT`、`blip-image-captioning` → `HF_BLIP_CAPTION`、`blip-vqa` → `HF_BLIP_VQA`、`grounding` 或 `dino` → `HF_GROUNDING`
4. **HuggingFace 路径回退**：包含 `/` 但不符合上述匹配的 ID → `HF_DETR`

这意味着常见模型无需显式注册即可使用。新架构需要扩展 `ModelCategory` 和 `_CATEGORY_HANDLER_MAP`。

---

## 接下来阅读什么

- [Handler 拓扑](/zh/architecture/handlers) — 模型到 handler 实现的映射关系
- [请求生命周期](/zh/architecture/request-flow) — 完整推理路径
- [性能基准](/zh/reference/benchmarks) — 延迟与吞吐量数据
- [REST API](/zh/api/rest-api) — 端点文档
- [配置参考](/zh/reference/configuration-reference) — 缓存与运行时设置
