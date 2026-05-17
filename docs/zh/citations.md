---
title: 参考文献与相关工作
---

# 参考文献与相关工作

YOLO-Toys 处在“实用服务化”和“上游模型研究”之间。这一页承担两件事：

1. 保存运行时所依赖模型家族与框架的引用材料
2. 把项目放到相邻开源系统的语境里理解

## 核心文献索引

| 领域 | 代表工作 | 在这里的意义 |
| --- | --- | --- |
| Transformer 检测 | DETR, Carion 等 (ECCV 2020) | 给运行时中的 transformer 检测能力提供谱系 |
| 开放词汇检测 | OWL-ViT, Minderer 等 (ECCV 2022) | 解释文本条件检测能力的来源 |
| Grounded Detection | Grounding DINO, Liu 等 (ECCV 2024) | 支撑短语级目标检测 |
| 视觉语言预训练 | BLIP, Li 等 (ICML 2023) | 支撑 caption 与 VQA 表面 |
| 服务运行时 | FastAPI、PyTorch、Transformers | 构成运行时底座与模型生态 |

## 值得与 YOLO-Toys 对照阅读的开源项目

| 项目 | 为什么值得对照 |
| --- | --- |
| Triton Inference Server | 理解性能优先、规模优先的服务假设 |
| TorchServe | 理解 PyTorch worker 式服务模式 |
| BentoML | 理解打包与部署工作流的不同侧重 |
| Ultralytics | 理解 YOLO 家族的上游执行模型 |

## 引用条目

### DETR

```bibtex
@inproceedings{carion2020detr,
  title = {End-to-End Object Detection with Transformers},
  author = {Carion, Nicolas and Massa, Francisco and Synnaeve, Gabriel and Usunier, Nicolas and Kirillov, Alexander and Zagoruyko, Sergey},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year = {2020},
  pages = {213--229}
}
```

### OWL-ViT

```bibtex
@inproceedings{minderer2022owlvit,
  title = {Simple Open-Vocabulary Object Detection with Vision Transformers},
  author = {Minderer, Matthias and others},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year = {2022}
}
```

### Grounding DINO

```bibtex
@inproceedings{liu2023grounding,
  title = {Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection},
  author = {Liu, Shilong and others},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year = {2024}
}
```

### BLIP

```bibtex
@inproceedings{li2022blip,
  title = {BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation},
  author = {Li, Junnan and others},
  booktitle = {International Conference on Machine Learning (ICML)},
  year = {2023}
}
```
