---
title: Academic Citations
---

# Academic Citations

If you use YOLO-Toys in your research, please cite the underlying models and frameworks. This page provides BibTeX entries for all models supported by the platform.

## YOLO Series

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

**Key paper**:

```bibtex
@article{jocher2022ultralytics,
  title = {Ultralytics YOLO},
  author = {Jocher, Glenn and others},
  year = {2022},
  url = {https://github.com/ultralytics/ultralytics},
  note = {YOLOv8 continues the YOLO family tradition with improved accuracy and efficiency}
}
```

### YOLOv5 (Precursor)

```bibtex
@software{jocher2022yolov5,
  title = {YOLOv5 by Ultralytics},
  author = {Jocher, Glenn},
  year = {2022},
  url = {https://github.com/ultralytics/yolov5},
  version = {7.0}
}
```

## DETR (DEtection TRansformer)

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

### Deformable DETR

```bibtex
@inproceedings{zhu2021deformable,
  title = {Deformable {DETR}: Deformable Transformers for End-to-End Object Detection},
  author = {Zhu, Xizhou and Su, Weijie and Lu, Lewei and Li, Bin and Wang, Xiaogang and Dai, Jifeng},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2021}
}
```

## OWL-ViT (Open-Vocabulary Detection)

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

**Model card**: [google/owlvit-base-patch32](https://huggingface.co/google/owlvit-base-patch32)

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

**Model card**: [IDEA-Research/grounding-dino-tiny](https://huggingface.co/IDEA-Research/grounding-dino-tiny)

## BLIP (Bootstrapping Language-Image Pre-training)

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

### BLIP-2

```bibtex
@inproceedings{li2023blip2,
  title = {{BLIP-2}: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models},
  author = {Li, Junnan and Li, Dongxu and Savarese, Silvio and Hoi, Steven},
  booktitle = {International Conference on Machine Learning (ICML)},
  year = {2023},
  pages = {19730--19742},
  publisher = {PMLR}
}
```

**Model cards**:
- [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)
- [Salesforce/blip-image-captioning-large](https://huggingface.co/Salesforce/blip-image-captioning-large)
- [Salesforce/blip-vqa-base](https://huggingface.co/Salesforce/blip-vqa-base)

## Foundational Frameworks

### Transformers (HuggingFace)

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

### FastAPI

```bibtex
@software{ramirez2018fastapi,
  title = {FastAPI},
  author = {Ram{\'\i}rez, Sebasti{\'a}n},
  year = {2018},
  url = {https://github.com/tiangolo/fastapi},
  license = {MIT}
}
```

## Citing YOLO-Toys

If you reference the YOLO-Toys platform itself in your work:

```bibtex
@software{yolotoys2024,
  title = {YOLO-Toys: A Multi-Model Vision Inference Platform},
  author = {YOLO-Toys Contributors},
  year = {2024},
  url = {https://github.com/your-org/yolo-toys},
  license = {MIT},
  note = {Multi-model vision inference platform with Handler Pattern,
           Registry Pattern, and TTL+LRU hybrid caching}
}
```

## Related Work

### Vision Transformers

```bibtex
@inproceedings{dosovitskiy2021vit,
  title = {An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale},
  author = {Dosovitskiy, Alexey and Beyer, Lucas and Kolesnikov, Alexander and Weissenborn, Dirk and Zhai, Xiaohua and Unterthiner, Thomas and Dehghani, Mostafa and Minderer, Matthias and Heigold, Georg and Gelly, Sylvain and Uszkoreit, Jakob and Houlsby, Neil},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2021}
}
```

### Vision-Language Models

```bibtex
@inproceedings{radford2021clip,
  title = {Learning Transferable Visual Models From Natural Language Supervision},
  author = {Radford, Alec and Kim, Jong Wook and Hallacy, Chris and Ramesh, Aditya and Goh, Gabriel and Agarwal, Sandhini and Sastry, Girish and Askell, Amanda and Mishkin, Pamela and Clark, Jack and Chen, Gretchen and Krueger, Gabe and Sutskever, Ilya},
  booktitle = {International Conference on Machine Learning (ICML)},
  year = {2021},
  pages = {8748--8763},
  publisher = {PMLR}
}
```

## Model License Summary

| Model | License | Commercial Use |
|-------|---------|----------------|
| YOLOv8 | AGPL-3.0 | Requires license for commercial use |
| DETR | Apache-2.0 | ✅ Yes |
| OWL-ViT | Apache-2.0 | ✅ Yes |
| Grounding DINO | Apache-2.0 | ✅ Yes |
| BLIP | BSD-3-Clause | ✅ Yes |

::: warning
YOLOv8 is licensed under AGPL-3.0, which requires open-sourcing derivative works. For commercial use without AGPL requirements, consider the [Ultralytics Enterprise License](https://ultralytics.com/license).
:::
