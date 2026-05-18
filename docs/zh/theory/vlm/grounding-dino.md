---
title: Grounding DINO
---

# Grounding DINO：短语定位与检测

Grounding DINO 结合了定位模型和检测模型的优势：可以用自然语言短语描述检测目标并保持高精度，同时支持开放词汇。

## 定位问题

**短语定位**：给定图像和文本描述，找到每个短语对应的图像区域。

示例：
```
文本："一只狗在公园里追逐红球"
短语：["狗", "红球", "公园"]
输出：[box_狗, box_球, box_公园]
```

这比开放词汇检测更精确，因为它利用了完整句子上下文。

## 架构

Grounding DINO 融合了：

1. **DINO**：自监督预训练的检测模型
2. **Grounding**：文本条件定位

```
图像 ────▶ 骨干网络 ────▶ 图像特征
                  │
                  │
文本 ────▶ BERT ──────▶ 文本特征
                  │
                  ▼
              特征融合（交叉注意力）
                  │
                  ▼
              检测头
                  │
                  ▼
              定位框
```

## 性能

| 模型 | COCO mAP | LVIS APr | RefCOCO 准确率 |
|------|----------|----------|----------------|
| OWL-ViT | 42.6 | 31.5 | - |
| GLIP | 49.8 | 27.0 | - |
| Grounding DINO | **52.5** | **33.8** | 85.6 |

## 何时使用 Grounding DINO

::: tip 推荐
- 带多目标的详细场景描述
- 短语级定位（不仅是目标名称）
- 高精度开放词汇检测
:::

::: warning 注意
对于纯检测任务比 YOLOv8 慢。简单开放词汇检测用 OWL-ViT。
:::

## 参考文献

1. Liu, S., et al. "Grounding DINO: Marrying DINO with Grounded Pre-Training." ECCV 2024.

---

## 接下来阅读

- [OWL-ViT](/zh/theory/vlm/owl-vit) 对比
- [BLIP](/zh/theory/vlm/blip) 图像描述
