---
title: "BLIP：图像描述与 VQA"
---

# BLIP：自举语言-图像预训练

BLIP（Bootstrapping Language-Image Pre-training）是统一视觉语言理解和生成的模型。YOLO-Toys 使用 BLIP 进行图像描述和视觉问答。

## 任务

### 图像描述

生成图像的自然语言描述：

```
输入：[图像]
输出："一只金毛猎犬在阳光明媚的公园里玩红球"
```

### 视觉问答（VQA）

回答关于图像内容的问题：

```
输入：[图像] + "狗的项圈是什么颜色？"
输出："蓝色"
```

## 架构

BLIP 使用统一架构，包含三个组件：

- **视觉编码器**：ViT 提取图像特征
- **文本编码器**：BERT 处理文本
- **多模态编码器**：融合图像和文本特征
- **理解头**：分类/回答问题
- **生成头**：自回归生成描述

## 关键创新

### 1. 自举训练

BLIP 用描述模型生成合成描述，再用学习过滤器过滤：

```python
# 自举循环
captions = generate_captions(images)
filtered = filter_captions(captions, images)
train_on(images, filtered)
```

### 2. 统一架构

同一模型处理理解（VQA）和生成（描述）。

## 模型变体

| 模型 | 参数量 | 描述质量 | VQA 准确率 |
|------|--------|----------|------------|
| BLIP-base | 223M | 好 | 75.0% |
| BLIP-large | 582M | 更好 | 78.3% |

## 性能

### 图像描述（COCO test）

| 模型 | BLEU-4 | METEOR | CIDEr |
|------|--------|--------|-------|
| BLIP | **39.9** | **32.1** | **133.2** |

### VQA（VQAv2 test-dev）

| 模型 | 准确率 |
|------|--------|
| BLIP | **78.3%** |

## 何时使用 BLIP

::: tip 图像描述
- 为无障碍生成 alt 文本
- 创建图像描述用于搜索
- 总结视觉内容
:::

::: tip 视觉问答
- 回答关于图像内容的问题
- 从图像提取特定信息
- 交互式图像探索
:::

## 参考文献

1. Li, J., et al. "BLIP: Bootstrapping Language-Image Pre-training." ICML 2023.

---

## 接下来阅读

- [OWL-ViT](/zh/theory/vlm/owl-vit) 开放词汇检测
- [Grounding DINO](/zh/theory/vlm/grounding-dino) 短语定位
