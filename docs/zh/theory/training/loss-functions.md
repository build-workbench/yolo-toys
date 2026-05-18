---
title: 损失函数
---

# 检测损失函数

理解损失函数对于诊断模型行为和调整推理参数至关重要。本章介绍 YOLO-Toys 中模型家族使用的关键损失。

## 为什么损失在推理时很重要

虽然损失在推理时不直接使用，但它们塑造了模型行为：

1. **置信度校准**：分类损失影响分数可靠性
2. **框质量**：回归损失决定定位精度
3. **阈值调整**：理解损失有助于设置置信度和 IoU 阈值

## YOLO 家族损失

### YOLOv1：平方和误差

YOLOv1 使用简单的平方和误差损失。

### YOLOv3–v5：二元交叉熵 + CIoU

分类用二元交叉熵，回归用 CIoU 损失：

$$
CIoU = IoU - \frac{\rho^2(b, b^{gt})}{c^2} - \alpha v
$$

CIoU 考虑重叠区域、中心距离和长宽比。

### YOLOv8：VFL + DFL + CIoU

YOLOv8 组合三种损失：

1. **VFL（变焦损失）**：分类的非对称焦点损失
2. **DFL（分布焦点损失）**：将框回归视为分布预测
3. **CIoU 损失**：框重叠的完整 IoU

## DETR 损失

### 二分图匹配损失

DETR 使用匈牙利匹配找到最优分配：

$$
\hat{\sigma} = \arg\min_{\sigma} \sum_i^N \mathcal{L}_{match}(y_i, \hat{y}_{\sigma(i)})
$$

### 匈牙利损失

匹配后，最终损失组合分类损失、L1 损失和 GIoU 损失。

## 对比损失（OWL-ViT、Grounding DINO）

### InfoNCE 损失

用于对比预训练：

$$
\mathcal{L} = -\frac{1}{N} \sum_i \log \frac{\exp(\text{sim}(I_i, T_i) / \tau)}{\sum_j \exp(\text{sim}(I_i, T_j) / \tau)}
$$

## 损失对比总结

| 模型 | 分类损失 | 回归损失 | 匹配方式 |
|------|----------|----------|----------|
| YOLOv5 | BCE | CIoU | 锚框式 |
| YOLOv8 | VFL | DFL + CIoU | 无锚框式 |
| DETR | CE | L1 + GIoU | 匈牙利 |
| OWL-ViT | BCE | L1 | 对比式 |
| BLIP | CE | — | 自回归 |

## 参考文献

1. Lin, T., et al. "Focal Loss for Dense Object Detection." ICCV 2017.
2. Zheng, Z., et al. "Distance-IoU Loss." AAAI 2020.

---

## 接下来阅读

- [YOLO 家族演进](/zh/theory/detection/yolo-family) 损失函数演进
