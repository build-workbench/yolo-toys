---
title: YOLO 家族演进
---

# YOLO 家族演进

从 YOLOv1 开创性的网格预测到 YOLOv8 的无锚框架构，YOLO 家族定义了实时目标检测的八年技术前沿。本章追溯每一代架构创新，了解它们如何让检测更快、更准、更灵活。

<FigureFrame
  title="图 1. YOLO 演进时间线"
  caption="每一代都引入了改进精度-速度权衡的架构创新。V8 的无锚框设计是自 V2 引入锚框以来最重大的范式转变。"
>
  <SvgRenderer src="/images/yolo-family-evolution.svg" alt="YOLO 家族演进时间线" title="YOLO 演进" />
</FigureFrame>

## 单阶段检测的核心洞见

在 YOLO 之前，目标检测遵循两阶段范式：先生成候选区域，再对每个区域分类。R-CNN 及其变体（Fast R-CNN、Faster R-CNN）精度高但计算昂贵。

YOLOv1 的洞见极其激进：**将检测视为单一回归问题**。不生成候选区域，而是将图像划分为网格，在一次前向传播中直接预测边界框和类别概率。

这一设计选择产生了深远影响：

- **速度**：推理 45 FPS，实现实时检测
- **全局上下文**：每个预测都能看到整张图像，减少背景误检
- **简洁性**：一个网络，一次传播，一个输出

## YOLOv1：奠基（2016）

### 架构

YOLOv1 使用修改过的 GoogLeNet 作为骨干网络，后接 24 个卷积层和 2 个全连接层。

### 局限性

1. **空间约束**：每个网格单元只预测 2 个框，限制了小目标或密集目标的检测
2. **无锚框**：直接预测 (x, y, w, h) 难以优化
3. **损失函数不平衡**：所有框权重相同，不考虑尺寸

### 结果

| 指标 | 值 |
|------|-----|
| mAP (VOC 2007) | 63.4% |
| FPS | 45 |
| 输入尺寸 | 448 × 448 |

## YOLOv2 / YOLO9000：锚框与更多（2017）

YOLOv2 用三大创新解决了 v1 的关键局限：

### 1. 锚框

不再预测绝对坐标，而是预测相对于预定义锚框的偏移：

```python
# YOLOv1: 直接预测
bx = sigmoid(tx)  # 约束到 [0, 1]

# YOLOv2: 基于锚框预测
bx = sigmoid(tx) + cx  # 相对于网格单元的偏移
by = sigmoid(ty) + cy
bw = pw * exp(tw)      # 从锚框缩放
bh = ph * exp(th)
```

锚框通过 k-means 聚类从训练数据学习，为目标形状提供更好的先验。

### 2. 批归一化

所有卷积层添加批归一化，mAP 提升 2%，并消除对 dropout 的需求。

### 3. 多尺度训练

在多种输入尺寸（320–608 像素）上训练，提高鲁棒性，允许推理时权衡速度和精度。

### 结果

| 指标 | 值 |
|------|-----|
| mAP (VOC 2007) | 76.8% |
| FPS | 67（288×288）|
| 多尺度 | ✓ |

## YOLOv3：特征金字塔（2018）

YOLOv3 引入使用特征金字塔网络（FPN）架构的多尺度预测：

### Darknet-53 骨干网络

受 ResNet 启发的 53 层网络，带有残差连接：

- 比 ResNet-101 快 3.8 倍
- ImageNet Top-5 准确率：93.5%

### 三尺度预测

在三个尺度（13×13、26×26、52×52）上预测，能够检测各种尺寸的目标。

### 结果

| 指标 | 值 |
|------|-----|
| mAP (COCO) | 33.0% |
| FPS | 30（320×320）|
| 尺度数 | 3 |

## YOLOv4：优化聚焦（2020）

YOLOv4 专注于训练优化而非架构变更：

### 免费技巧包

不影响推理速度但提高精度的技术：

- **Mosaic 数据增强**：将 4 张训练图像组合为一张
- **DropBlock**：丢弃特征图的连续区域
- **类别标签平滑**：正则化类别预测

### 特殊技巧包

以最小速度代价提高精度的技术：

- **CSPNet**：跨阶段部分连接减少计算
- **PANet**：路径聚合网络改善特征融合
- **SAM**：空间注意力模块

### 结果

| 指标 | 值 |
|------|-----|
| mAP (COCO) | 43.5% |
| FPS | 38 (V100) |
| 输入尺寸 | 608 × 608 |

## YOLOv5：生产就绪（2020）

YOLOv5 在 v4 之后不久由 Ultralytics 发布，专注于工程质量：

### 原生 PyTorch

首个纯 PyTorch 实现的 YOLO，支持：

- 无需 Darknet 依赖即可轻松部署
- ONNX 导出实现跨平台推理
- 原生分布式训练

### 自动锚框学习

锚框自动为你的数据集优化：

```python
# 自动锚框：k-means + 遗传进化
anchors = kmeans(boxes, k=9)
anchors = genetic_evolution(anchors, fitness=mAP)
```

### 模型缩放

YOLOv5n/s/m/l/x 的一致缩放规则：

| 模型 | 参数量 | mAP | FPS |
|------|--------|-----|-----|
| YOLOv5n | 1.9M | 28.0 | 140 |
| YOLOv5s | 7.2M | 37.4 | 100 |
| YOLOv5m | 21.2M | 45.4 | 70 |
| YOLOv5l | 46.5M | 49.0 | 50 |
| YOLOv5x | 86.7M | 50.7 | 30 |

## YOLOv8：无锚框革命（2023）

YOLOv8 代表自 v2 以来最重大的架构变革：**无锚框检测**。

### 为什么无锚框？

锚框式检测有固有问题：

1. **超参数敏感**：锚框设计显著影响性能
2. **目标形状不匹配**：固定锚框可能不适合异常目标
3. **冗余预测**：每个位置多个锚框产生重复

无锚框方法直接预测目标中心，将检测视为关键点估计。

### 解耦头

YOLOv8 将分类和回归分离为独立分支：

```
骨干网络特征
    │
    ├──▶ 分类分支 ───▶ 类别分数
    │
    └──▶ 回归分支 ───▶ 边界框 (DFL)

任务间无共享权重
```

### C2f 模块

用更高效的特征融合设计替代 CSP 块。

### 损失函数

YOLOv8 组合三种损失：

1. **VFL（变焦损失）**：带焦点加权的分类
2. **DFL（分布焦点损失）**：将框回归视为分布预测
3. **CIoU 损失**：完整 IoU 用于框重叠

### 模型缩放（v8）

| 模型 | 参数量 | mAP | FPS |
|------|--------|-----|-----|
| YOLOv8n | 3.2M | 37.3 | 80 |
| YOLOv8s | 11.2M | 44.9 | 60 |
| YOLOv8m | 25.9M | 50.2 | 40 |
| YOLOv8l | 43.7M | 52.9 | 30 |
| YOLOv8x | 68.2M | 53.9 | 20 |

## 架构对比

| 特性 | v1 | v2 | v3 | v4 | v5 | v8 |
|------|----|----|----|----|----|----|
| 锚框 | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| FPN | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| 骨干网络 | GoogLeNet | Darknet-19 | Darknet-53 | CSPDarknet | CSPDarknet | CSPDarknet |
| 框架 | Darknet | Darknet | Darknet | Darknet | PyTorch | PyTorch |
| 解耦头 | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |

## 如何选择 YOLO

::: tip 实时边缘部署
**YOLOv8n** — 最小模型，最快推理，适合移动端/嵌入式
:::

::: tip 生产 API 服务
**YOLOv8s/m** — 精度速度均衡，适合大多数场景
:::

::: tip 最高精度
**YOLOv8l/x** — 最高 mAP，精度优先时使用
:::

::: tip 向后兼容
**YOLOv5** — 成熟生态，丰富文档，稳定 ONNX 导出
:::

## 参考文献

1. Redmon, J., et al. "You Only Look Once: Unified, Real-Time Object Detection." CVPR 2016.

2. Redmon, J., Farhadi, A. "YOLO9000: Better, Faster, Stronger." CVPR 2017.

3. Redmon, J., Farhadi, A. "YOLOv3: An Incremental Improvement." arXiv 2018.

4. Bochkovskiy, A., et al. "YOLOv4: Optimal Speed and Accuracy of Object Detection." arXiv 2020.

5. Jocher, G., et al. "Ultralytics YOLOv5." GitHub 2020.

6. Jocher, G., et al. "Ultralytics YOLOv8." GitHub 2023.

---

## 接下来阅读

- [DETR 架构](/zh/theory/detection/detr-transformer) 了解基于 Transformer 的替代方案
- [检测范式对比](/zh/theory/detection/detection-paradigms) 系统性比较
- [模型矩阵](/zh/reference/models) 实用选择指南
