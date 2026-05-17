---
title: Bibliography and Related Work
---

# Bibliography and Related Work

YOLO-Toys sits at the intersection of practical serving and upstream model research. This page does two jobs:

1. preserve citation material for the model families and frameworks the runtime depends on
2. position the project among adjacent open-source systems that solve related serving problems

## Core bibliography

| Area | Primary work | Why it matters here |
| --- | --- | --- |
| Detection transformers | DETR, Carion et al. (ECCV 2020) | establishes the transformer-based detection lineage in the runtime |
| Open-vocabulary detection | OWL-ViT, Minderer et al. (ECCV 2022) | frames text-conditioned detection support |
| Grounded detection | Grounding DINO, Liu et al. (ECCV 2024) | supports phrase-grounded object detection |
| Vision-language pretraining | BLIP, Li et al. (ICML 2023) | underpins captioning and VQA surfaces |
| Serving framework | FastAPI, PyTorch, Transformers | provide the runtime substrate and model ecosystem |

## Related open-source projects worth reading alongside YOLO-Toys

| Project | Why compare it |
| --- | --- |
| Triton Inference Server | for scale-first, performance-first serving assumptions |
| TorchServe | for worker-based PyTorch serving patterns |
| BentoML | for packaging and deployment workflow comparisons |
| Ultralytics | for the upstream YOLO family execution model |

## Citation entries

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
