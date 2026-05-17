---
title: Bibliography and Related Work
---

# Bibliography and Related Work

YOLO-Toys sits at the intersection of practical serving and upstream model research. This page does two jobs:

1. preserve citation material for the model families and frameworks the runtime depends on
2. position the project among adjacent open-source systems that solve related serving problems

## Core bibliography

| Area | Primary work | Why it matters here |
|------|-------------|---------------------|
| YOLO family | Redmon et al. (CVPR 2016); Jocher et al. (Ultralytics 2023) | establishes the single-shot detection lineage that dominates the runtime's throughput-optimized path |
| Detection transformers | DETR, Carion et al. (ECCV 2020) | establishes the transformer-based detection lineage in the runtime |
| Open-vocabulary detection | OWL-ViT, Minderer et al. (ECCV 2022) | frames text-conditioned detection support |
| Grounded detection | Grounding DINO, Liu et al. (ECCV 2024) | supports phrase-grounded object detection |
| Vision-language pretraining | BLIP, Li et al. (ICML 2023) | underpins captioning and VQA surfaces |
| Serving framework | FastAPI, Ramalho et al. (2019); PyTorch, Paszke et al. (NeurIPS 2019) | provide the runtime substrate and model ecosystem |
| Async web framework | Starlette, Archer (2018) | the ASGI foundation that FastAPI builds on |
| Configuration patterns | Pydantic Settings, Colucci et al. (2022) | enables type-safe environment-variable ingestion |

### YOLO

```bibtex
@article{redmon2016yolo,
  title={You Only Look Once: Unified, Real-Time Object Detection},
  author={Redmon, Joseph and Divvala, Santosh and Girshick, Ross and Farhadi, Ali},
  journal={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2016},
  pages={779--788}
}
```

### YOLOv8 (Ultralytics)

```bibtex
@software{jocher2023ultralytics,
  title={Ultralytics YOLOv8},
  author={Jocher, Glenn and Chaurasia, Ayush and Qiu, Jing},
  year={2023},
  url={https://github.com/ultralytics/ultralytics}
}
```

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

### FastAPI

```bibtex
@software{ramalho2019fastapi,
  title={FastAPI},
  author={Ramalho, Sebastián},
  year={2019},
  url={https://github.com/tiangolo/fastapi}
}
```

### PyTorch

```bibtex
@inproceedings{paszke2019pytorch,
  title={PyTorch: An Imperative Style, High-Performance Deep Learning Library},
  author={Paszke, Adam and Gross, Sam and Massa, Francisco and Lerer, Adam and Bradbury, James and Chanan, Gregory and Killeen, Trevor and Lin, Zeming and Gimelshein, Natalia and Antiga, Luca and others},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  year={2019}
}
```

## Related open-source projects worth reading alongside YOLO-Toys

| Project | Why compare it | GitHub |
|---------|---------------|--------|
| Triton Inference Server | for scale-first, performance-first serving assumptions | `triton-inference-server/server` |
| TorchServe | for worker-based PyTorch serving patterns | `pytorch/serve` |
| BentoML | for packaging and deployment workflow comparisons | `bentoml/BentoML` |
| Ultralytics | for the upstream YOLO family execution model | `ultralytics/ultralytics` |
| vLLM | for a reference PagedAttention-based LLM serving design | `vllm-project/vllm` |
| Ray Serve | for actor-based distributed serving patterns | `ray-project/ray` |
| ONNX Runtime | for cross-platform model acceleration and deployment | `microsoft/onnxruntime` |
| TensorRT | for NVIDIA GPU-optimized inference acceleration | `NVIDIA/TensorRT` |

### Comparative reading guide

**Triton Inference Server** is the industry standard for high-scale model serving. It supports multiple backends (TensorRT, ONNX, PyTorch, TensorFlow), dynamic batching, and multi-GPU scheduling. YOLO-Toys is intentionally narrower: it serves only vision models, it uses a single Python process, and it optimizes for developer readability rather than throughput maximization.

**TorchServe** is PyTorch's official serving solution. It uses a worker-per-model architecture with a model-archiver packaging format. YOLO-Toys differs by keeping all handlers in a single runtime process with a shared cache, avoiding the inter-process communication overhead that TorchServe incurs.

**BentoML** is a model serving framework with strong packaging and deployment ergonomics. It abstracts the model artifact and service definition into a deployable unit. YOLO-Toys is more opinionated: it does not try to be a general-purpose serving framework; it is a purpose-built runtime for heterogeneous vision inference.

**vLLM** is included here despite being LLM-focused because its PagedAttention memory management and continuous batching are relevant research directions for vision serving. The vision serving community has not yet produced an equivalent of vLLM's memory efficiency.

## Design pattern references

The architecture of YOLO-Toys draws on established software engineering patterns:

| Pattern | Where it appears | Reference |
|---------|-----------------|-----------|
| Strategy / Template Method | `BaseHandler` + subclasses | Gamma et al., *Design Patterns* (1994) |
| Registry | `HandlerRegistry` | Fowler, *Patterns of Enterprise Application Architecture* (2002) |
| Deep Module | `LoadedModel` hides `processor` | Martin, *Clean Architecture* (2017) |
| Protocol / Interface Segregation | `ModelManagerConfig` protocol | PEP 544 — Protocols (2017) |
| Adapter | `SettingsModelManagerConfig` | Gamma et al., *Design Patterns* (1994) |

## What to read next

- [Evolution](/en/research/evolution) for how these influences shaped the runtime's design decisions
- [Comparisons](/en/reference/comparisons) for a decision matrix when choosing a serving system
