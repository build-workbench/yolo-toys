---
title: "OWL-ViT：开放词汇检测"
---

# OWL-ViT：开放词汇目标检测

OWL-ViT（Open-World Localization - Vision Transformer）使用自然语言描述检测任意目标类别。不同于传统检测器受限于固定类别集，OWL-ViT 可以检测"蓝色背包"或"骑独轮车的人"而无需在这些特定类别上训练。

<FigureFrame
  title="图 1. OWL-ViT 架构"
  caption="OWL-ViT 使用双塔设计：图像编码器提取视觉特征，文本编码器处理自然语言查询。对比预训练对齐这两种模态，实现文本条件检测。"
>
  <SvgRenderer src="/images/owl-vit-mechanism.svg" alt="OWL-ViT 架构图" title="OWL-ViT 架构" />
</FigureFrame>

## 开放词汇问题

传统目标检测器有根本局限：**固定类别体系**。

| 检测器 | 类别数 | 训练数据 |
|--------|--------|----------|
| YOLOv8 | 80 (COCO) | COCO train2017 |
| Faster R-CNN | 80 | COCO train2017 |
| DETR | 80 | COCO train2017 |

如果需要检测：
- "戴红帽子的人"（不在 COCO 中）
- "特定产品 SKU"（领域特定）
- "损坏的汽车保险杠"（需要细粒度推理）

OWL-ViT 通过学习图像和文本的**共享嵌入空间**，然后用文本查询条件检测来解决。

## 架构

### 双塔设计

OWL-ViT 遵循 CLIP 的双塔架构：

- **图像塔**：ViT-L/14 处理图像为特征序列
- **文本塔**：Transformer 处理文本查询为嵌入

**与 CLIP 的关键区别**：OWL-ViT 保留空间信息（H' × W'），不仅是全局池化向量。

### 检测头

轻量检测头组合图像特征和文本嵌入：

```python
# 对每个图像块 (i) 和文本查询 (q)：
logit[i, q] = sigmoid(image_feat[i] · text_embed[q])

# 每个块的框预测：
box[i] = MLP(image_feat[i])  # (cx, cy, w, h)
```

## 对比预训练

OWL-ViT 在图文对上预训练（类似 CLIP）学习对齐嵌入：

### 训练目标

对比损失使匹配的图文对相似，不匹配的不相似。

### 数据规模

预训练数据：
- **LAION-400M**：4 亿图文对
- **LAION-2B**：20 亿图文对（OWL-ViT v2）

## 推理：文本条件检测

推理时提供文本查询：

```python
# 示例：检测特定目标
queries = ["一只猫", "一只狗", "一辆红色汽车", "骑自行车的人"]

# 编码查询
text_embeddings = text_encoder(queries)  # [4, d]

# 编码图像
image_features = image_encoder(image)  # [H', W', d]

# 计算相似度
logits = sigmoid(image_features @ text_embeddings.T)  # [H', W', 4]

# 阈值并提取框
for q_idx, query in enumerate(queries):
    scores = logits[:, :, q_idx]
    boxes = extract_boxes(scores, threshold=0.1)
    print(f"{query}: {len(boxes)} 个检测结果")
```

## 与传统检测对比

| 方面 | 传统（YOLO）| OWL-ViT |
|------|-------------|---------|
| 类别 | 固定（80 COCO）| 开放（任意文本）|
| 训练 | 有监督 | 对比预训练 |
| 推理 | 类别索引 | 文本查询 |
| 新类别 | ✗ | ✓ |
| 速度 | 快（10ms）| 较慢（100ms）|
| 已知类别精度 | 高 | 中等 |
| 新类别精度 | N/A | 合理 |

## 性能

### LVIS 基准（开放词汇）

| 模型 | APr（稀有）| APc（常见）| APf（频繁）|
|------|------------|------------|------------|
| Faster R-CNN | 1.3 | 9.5 | 15.5 |
| OWL-ViT | **31.5** | 32.0 | 32.5 |

*APr = 稀有类别平均精度（训练时未见）*

## 何时使用 OWL-ViT

::: tip 推荐
- 无训练数据的新类别检测
- 自然语言快速原型
- 领域特定检测（医疗、工业、零售）
:::

::: warning 不推荐
- 实时应用（改用 YOLO）
- 有训练数据的固定类别体系
- 已知类别上的最高精度
:::

## 参考文献

1. Minderer, M., et al. "Simple Open-Vocabulary Object Detection with Vision Transformers." ECCV 2022.

---

## 接下来阅读

- [Grounding DINO](/zh/theory/vlm/grounding-dino) 另一种开放词汇方法
- [BLIP](/zh/theory/vlm/blip) 图像描述
