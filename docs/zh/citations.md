---
title: 学术引用
---

# 学术引用

如果您在研究中使用 YOLO-Toys，请引用底层模型和框架。本页面提供平台支持的所有模型的 BibTeX 条目。

## YOLO 系列

### YOLOv8

```bibtex
@software{ultralytics2023yolov8,
  title = {Ultralytics YOLOv8},
  author = {Jocher, Glenn and Chaurasia, Ayush and Qiu, Jing},
  year = {2023},
  url = {https://github.com/ultralytics/ultralytics},
  version = {8.0.0},
  license = {AGPL-3.0}
}
```

## DETR（DEtection TRansformer）

### DETR

```bibtex
@inproceedings{carion2020detr,
  title = {End-to-End Object Detection with Transformers},
  author = {Carion, Nicolas and Massa, Francisco and Synnaeve, Gabriel and Usunier, Nicolas and Kirillov, Alexander and Zagoruyko, Sergey},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year = {2020},
  pages = {213--229},
  publisher = {Springer},
  doi = {10.1007/978-3-030-58452-8_13}
}
```

## OWL-ViT（开放词汇检测）

### OWL-ViT

```bibtex
@inproceedings{minderer2022owlvit,
  title = {Simple Open-Vocabulary Object Detection with Vision Transformers},
  author = {Minderer, Matthias and Gritsenko, Alexey and Stone, Austin and Neumann, Maximilian and Weissenborn, Dirk and Dosovitskiy, Alexey and Mahendran, Aravindh and Arnab, Anurag and Dehghani, Mostafa and Shen, Zhuoran and Wang, Xiaoqian and Xiao, Xiaohua and Wirges, Shannon and Beyer, Lucas and Houlsby, Neil},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year = {2022},
  pages = {728--755},
  publisher = {Springer},
  doi = {10.1007/978-3-031-20080-9_42}
}
```

## Grounding DINO

### Grounding DINO

```bibtex
@inproceedings{liu2023grounding,
  title = {Grounding {DINO}: Marrying {DINO} with Grounded Pre-Training for Open-Set Object Detection},
  author = {Liu, Shilong and Zeng, Zhaoyang and Ren, Tianhe and Li, Feng and Zhang, Hao and Yang, Jie and Li, Chunyuan and Yang, Jianwei and Su, Hang and Zhu, Jun and Zhang, Lei},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year = {2024},
  pages = {386--404},
  publisher = {Springer}
}
```

## BLIP（Bootstrapping Language-Image Pre-training）

### BLIP

```bibtex
@inproceedings{li2022blip,
  title = {{BLIP}: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation},
  author = {Li, Junnan and Li, Dongxu and Savarese, Silvio and Hoi, Steven},
  booktitle = {International Conference on Machine Learning (ICML)},
  year = {2023},
  pages = {12888--12900},
  publisher = {PMLR}
}
```

## 基础框架

### Transformers（HuggingFace）

```bibtex
@inproceedings{wolf2020transformers,
  title = {Transformers: State-of-the-Art Natural Language Processing},
  author = {Wolf, Thomas and Debut, Lysandre and Sanh, Victor and Chaumond, Julien and Delangue, Clement and Moi, Anthony and Cistac, Pierric and Rault, Tim and Louf, Remi and Funtowicz, Morgan and Davison, Joe and Shleifer, Sam and von Platen, Patrick and Ma, Clara and Jernite, Yacine and Plu, Julien and Xu, Can and Le Scao, Teven and Gugger, Sylvain and Drame, Mariama and Lhoest, Quentin and Rush, Alexander},
  booktitle = {Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations},
  year = {2020},
  pages = {38--45},
  doi = {10.18653/v1/2020.emnlp-demos.6}
}
```

### PyTorch

```bibtex
@inproceedings{paszke2019pytorch,
  title = {{PyTorch}: An Imperative Style, High-Performance Deep Learning Library},
  author = {Paszke, Adam and Gross, Sam and Massa, Francisco and Lerer, Adam and Bradbury, James and Chanan, Gregory and Killeen, Trevor and Lin, Zeming and Gimelshein, Natalia and Antiga, Luca and Desmaison, Alban and Kopf, Andreas and Yang, Edward and DeVito, Zachary and Raison, Martin and Tejani, Alykhan and Chilamkurthy, Sasank and Steiner, Benoit and Fang, Lu and Bai, Junjie and Chintala, Soumith},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2019},
  pages = {8024--8035}
}
```

## 引用 YOLO-Toys

如果您在作品中引用 YOLO-Toys 平台本身：

```bibtex
@software{yolotoys2024,
  title = {YOLO-Toys: A Multi-Model Vision Inference Platform},
  author = {YOLO-Toys Contributors},
  year = {2024},
  url = {https://github.com/your-org/yolo-toys},
  license = {MIT},
  note = {多模型视觉推理平台，采用 Handler 模式、
           Registry 模式和 TTL+LRU 混合缓存}
}
```

## 模型许可摘要

| 模型 | 许可证 | 商业使用 |
|------|--------|----------|
| YOLOv8 | AGPL-3.0 | 商业使用需要许可证 |
| DETR | Apache-2.0 | ✅ 可以 |
| OWL-ViT | Apache-2.0 | ✅ 可以 |
| Grounding DINO | Apache-2.0 | ✅ 可以 |
| BLIP | BSD-3-Clause | ✅ 可以 |

::: warning
YOLOv8 采用 AGPL-3.0 许可，要求开源衍生作品。如需商业使用而无需 AGPL 要求，请考虑 [Ultralytics Enterprise License](https://ultralytics.com/license)。
:::
