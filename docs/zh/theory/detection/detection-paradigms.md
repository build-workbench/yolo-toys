---
title: 检测范式对比
---

# 检测范式：系统性对比

本章对三大检测范式提供统一对比：锚框式、无锚框式和基于 Transformer 的方法。

## 历史脉络

```
2014 ────────────────────────────────────────────────────── 2024

锚框式                          无锚框式               基于 Transformer
──────                          ────────               ────────────────

Faster R-CNN (2015)             CenterNet (2019)       DETR (2020)
SSD (2016)                      FCOS (2019)            Deformable DETR
YOLOv2-v5 (2017-2020)           YOLOv8 (2023)          DINO (2022)
RetinaNet (2017)                RTMDet (2022)          Co-DETR (2023)
```

## 定量对比

### COCO val2017 mAP

| 模型 | 范式 | mAP | FPS (V100) | 参数量 |
|------|------|-----|------------|--------|
| YOLOv5l | 锚框式 | 49.0 | 50 | 46.5M |
| YOLOv8l | 无锚框式 | 52.9 | 30 | 43.7M |
| DETR-R101 | Transformer | 43.5 | 10 | 60M |
| DINO-R50 | Transformer | 50.4 | 12 | 47M |

## 何时选择哪种范式

### 锚框式（YOLOv5）

- 需要最大推理速度
- 目标长宽比一致
- 需要成熟工具和文档

### 无锚框式（YOLOv8）

- 目标长宽比多样
- 希望更少超参数
- 正在启动新项目（推荐默认选择）

### Transformer（DETR）

- 检测大型、分布均匀的目标
- 需要全局上下文推理
- 进行检测研究

## 参考文献

1. Ren, S., et al. "Faster R-CNN." NeurIPS 2015.
2. Carion, N., et al. "End-to-End Object Detection with Transformers." ECCV 2020.

---

## 接下来阅读

- [YOLO 家族演进](/zh/theory/detection/yolo-family) 详细 YOLO 历史
- [DETR 架构](/zh/theory/detection/detr-transformer) Transformer 细节
- [模型矩阵](/zh/reference/models) 实用选择
