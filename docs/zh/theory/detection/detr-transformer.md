---
title: DETR 架构
---

# DETR：检测 Transformer

DETR（Detection Transformer）代表了目标检测的范式转变：通过将检测框架为直接集合预测问题，消除了锚框和非极大值抑制（NMS）等手工设计组件的需求。

<FigureFrame
  title="图 1. DETR 架构"
  caption="DETR 使用 CNN 骨干网络提取特征，后接 Transformer 编码器-解码器。目标查询学习关注图像区域并直接预测边界框。"
>
  <SvgRenderer src="/images/detr-architecture.svg" alt="DETR 架构图" title="DETR 架构" />
</FigureFrame>

## 集合预测的洞见

传统检测器预测大量边界框（数千个），然后用 NMS 过滤。这产生几个问题：

1. **重复预测**：NMS 是启发式方法，可能移除真阳性
2. **锚框设计**：需要仔细调整锚框尺寸和长宽比
3. **后处理**：检测不是真正的端到端

DETR 的洞见：**将检测视为集合预测问题**。模型直接输出固定大小的预测集合，每个"目标查询"对应一个预测，无需后处理。

## 架构概览

### 骨干网络（CNN）

DETR 使用标准 CNN 骨干网络（ResNet-50 或 ResNet-101）提取特征：

```
输入：H × W × 3
         ↓
ResNet 骨干网络
         ↓
输出：H/32 × W/32 × 2048
```

### Transformer 编码器

编码器用自注意力处理展平的特征图：

```
特征 + 位置编码
    │
    ▼
自注意力 ─── 每个位置关注所有其他位置
    │
    ▼
FFN ──────── 逐位置变换
    │
    × 6 层
```

### Transformer 解码器

解码器接收**目标查询**——将变成最终预测的学习嵌入：

```
目标查询（N 个学习向量）
    │
    ▼
自注意力 ─── 查询相互关注
    │
    ▼
交叉注意力 ─── 查询关注编码器输出
    │
    ▼
FFN
    │
    × 6 层
```

**核心洞见**：目标查询通过交叉注意力竞争不同的图像区域。每个查询学习专门检测特定位置的目标。

### 预测头

两个并行 FFN 产生最终输出：

- **类别头**：N × (C + 1) 类别预测（含"无目标"）
- **框头**：N × 4 边界框坐标（center_x, center_y, width, height）

## 二分图匹配损失

核心创新是损失函数。DETR 使用**匈牙利匹配**找到预测和真值之间的最优分配：

### 步骤 1：匈牙利匹配

找到最小化匹配代价的排列 σ：

$$
\hat{\sigma} = \arg\min_{\sigma} \sum_i^N \mathcal{L}_{match}(y_i, \hat{y}_{\sigma(i)})
$$

### 步骤 2：损失计算

匹配后计算最终损失，组合分类损失和框损失。

## 无 NMS，无锚框

二分图匹配损失确保每个真值目标恰好匹配一个预测。这消除了：

1. **重复预测**：每个查询最多产生一个框
2. **锚框调整**：目标查询是学习的，不是设计的
3. **NMS 启发式**：集合预测自然处理重复

## 性能

| 模型 | 骨干网络 | mAP (COCO) | FPS |
|------|----------|------------|-----|
| DETR | ResNet-50 | 42.0 | 12 |
| DETR | ResNet-101 | 43.5 | 10 |
| DETR-DC5 | ResNet-101 | 47.0 | 8 |

### 优势

- **大目标**：DETR 擅长检测大目标
- **无手工组件**：完全学习的检测
- **架构清晰**：易于理解和扩展

### 劣势

- **小目标**：小目标检测困难
- **训练时间**：需要 500 个 epoch 完整训练
- **收敛**：比锚框方法收敛慢

## 何时使用 DETR

::: tip 密集场景
DETR 在目标分布均匀且较大时表现出色。用于场景理解任务。
:::

::: tip 研究
DETR 的清晰架构使其成为检测和集合预测研究的理想选择。
:::

::: warning 小目标
对于小目标检测，考虑 Deformable DETR 或 YOLOv8。
:::

## 参考文献

1. Carion, N., et al. "End-to-End Object Detection with Transformers." ECCV 2020.

---

## 接下来阅读

- [检测范式对比](/zh/theory/detection/detection-paradigms) 比较 DETR 和 YOLO
- [YOLO 家族演进](/zh/theory/detection/yolo-family) 了解锚框谱系
- [模型矩阵](/zh/reference/models) 实用选择
