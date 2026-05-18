---
title: 理论与算法
---

# 理论与算法

本章深入介绍 YOLO-Toys 所服务模型的算法背景。理解这些基础知识有助于选择合适的模型、调整推理参数以及权衡性能取舍。

<FigureFrame
  title="图 1. 模型家族全景"
  caption="YOLO-Toys 服务于五个不同的模型家族，每个家族都有独特的架构假设、训练范式和推理特性。"
>
  <SvgRenderer src="/images/hero-architecture.svg" alt="模型家族全景" title="模型家族" />
</FigureFrame>

## 章节结构

### [检测算法](/zh/theory/detection/)

目标检测是大多数 YOLO-Toys 用例的核心任务。本节涵盖：

- **[YOLO 家族演进](/zh/theory/detection/yolo-family)** — 从 YOLOv1 的网格预测到 YOLOv8 的无锚框架构，追溯八年单阶段检测创新历程
- **[DETR 架构](/zh/theory/detection/detr-transformer)** — Transformer 如何实现无需锚框和 NMS 的端到端检测
- **[检测范式对比](/zh/theory/detection/detection-paradigms)** — 对比锚框式、无锚框式和基于 Transformer 的方法

### [视觉语言模型](/zh/theory/vlm/)

开放词汇检测和图像理解模型：

- **[OWL-ViT](/zh/theory/vlm/owl-vit)** — 基于对比预训练的文本条件检测
- **[Grounding DINO](/zh/theory/vlm/grounding-dino)** — 融合视觉语言特征的短语定位
- **[BLIP](/zh/theory/vlm/blip)** — 图像描述与视觉问答

### [训练背景](/zh/theory/training/)

理解推理之前发生了什么：

- **[损失函数](/zh/theory/training/loss-functions)** — 检测损失、对比损失及其梯度

## 为什么这些很重要

YOLO-Toys 抽象了模型家族的差异，但这种抽象不是免费的。理解底层架构有助于：

1. **选择正确的模型** — YOLOv8 擅长吞吐量；DETR 更适合密集场景；OWL-ViT 可检测新类别
2. **智能调参** — 置信度阈值、IoU 阈值和 NMS 设置在不同家族中有不同含义
3. **诊断失败** — 为什么 OWL-ViT 漏检了这个目标？为什么 DETR 在这张图上更慢？
4. **规划扩展** — 添加新模型家族需要什么？

## 阅读路径

::: tip 运维人员
从 [检测范式对比](/zh/theory/detection/detection-paradigms) 开始获取概览，然后深入了解你部署的特定模型家族。
:::

::: tip 贡献者
阅读 [YOLO 家族演进](/zh/theory/detection/yolo-family) 和 [DETR 架构](/zh/theory/detection/detr-transformer) 来理解 YOLO-Toys 标准化的架构模式。
:::

::: tip 研究人员
[视觉语言模型](/zh/theory/vlm/) 章节涵盖检测生态中最新的成员。这些模型代表了开放词汇感知的前沿。
:::

## 接下来阅读

- [YOLO 家族演进](/zh/theory/detection/yolo-family) 了解经典检测谱系
- [OWL-ViT](/zh/theory/vlm/owl-vit) 了解开放词汇检测
- [模型选择指南](/zh/reference/models) 获取实用决策树
