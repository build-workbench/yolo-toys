---
title: Bibliography and Related Work
---

# Bibliography and Related Work

YOLO-Toys sits at the intersection of practical serving infrastructure and upstream model research. This page serves two purposes:

1. **Canonical bibliography** — citable references for the model families, frameworks, and patterns the runtime depends on
2. **Comparative positioning** — situating YOLO-Toys among adjacent open-source systems solving related serving problems

---

## Core bibliography

| Area | Primary work | Relevance to YOLO-Toys |
|------|-------------|------------------------|
| Object detection (anchor-based) | Redmon et al. (CVPR 2016) | foundational YOLO lineage that dominates the throughput-optimized path |
| Object detection (anchor-free) | Jocher et al. (Ultralytics, 2023) | the execution model for YOLOv8 anchor-free detection |
| Detection transformers | Carion et al. (ECCV 2020) | transformer-based detection lineage — DETR handler |
| Open-vocabulary detection | Minderer et al. (ECCV 2022) | text-conditioned detection support via OWL-ViT handler |
| Grounded detection | Liu et al. (ECCV 2024) | phrase-grounding support via Grounding DINO handler |
| Vision-language pretraining | Li et al. (ICML 2023) | captioning and VQA support via BLIP handler |
| Serving framework | Ramalho (2019); Paszke et al. (NeurIPS 2019) | runtime substrate and model execution environment |
| Async web framework | Archer (2018) | ASGI foundation powering FastAPI |
| Configuration patterns | Colucci et al. (2022) | type-safe environment-variable ingestion |
| Design patterns | Gamma et al. (1994) | Strategy, Registry, Adapter patterns in handler topology |

---

## Detection algorithms

### YOLOv1 — Original YOLO

<CitationBlock
  :number="1"
  authors="Redmon, J., Divvala, S., Girshick, R., and Farhadi, A."
  title="You Only Look Once: Unified, Real-Time Object Detection"
  venue="IEEE Conference on Computer Vision and Pattern Recognition (CVPR)"
  year="2016"
  url="https://arxiv.org/abs/1506.02640"
/>

The original YOLO paper reframed detection as a single regression problem: divide the image into an S×S grid, predict bounding boxes and class probabilities from each grid cell in one forward pass. This unified formulation traded recall on small objects for dramatically better throughput — a trade-off that remained central to the YOLO lineage for years.

```bibtex
@inproceedings{redmon2016yolo,
  title     = {You Only Look Once: Unified, Real-Time Object Detection},
  author    = {Redmon, Joseph and Divvala, Santosh and Girshick, Ross and Farhadi, Ali},
  booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2016},
  pages     = {779--788}
}
```

### YOLOv8 — Anchor-free YOLO

<CitationBlock
  :number="2"
  authors="Jocher, G., Chaurasia, A., and Qiu, J."
  title="Ultralytics YOLOv8"
  venue="Software release"
  year="2023"
  url="https://github.com/ultralytics/ultralytics"
/>

YOLOv8 is the version served by YOLO-Toys. It introduces an anchor-free detection head with decoupled classification and regression branches, C2f backbone blocks (Cross Stage Partial with two bottlenecks), and native multi-task support for detection, segmentation, and pose in a single architecture family. The `YOLOHandler` in YOLO-Toys calls `ultralytics.YOLO(model_id)` directly and delegates all family-specific logic to the Ultralytics library.

```bibtex
@software{jocher2023ultralytics,
  title  = {Ultralytics YOLOv8},
  author = {Jocher, Glenn and Chaurasia, Ayush and Qiu, Jing},
  year   = {2023},
  url    = {https://github.com/ultralytics/ultralytics}
}
```

### DETR — End-to-End Object Detection with Transformers

<CitationBlock
  :number="3"
  authors="Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A., and Zagoruyko, S."
  title="End-to-End Object Detection with Transformers"
  venue="European Conference on Computer Vision (ECCV)"
  year="2020"
  url="https://arxiv.org/abs/2005.12872"
/>

DETR eliminates anchors and NMS by treating detection as a set prediction problem. A Transformer encoder-decoder with learned object queries produces a fixed-size set of predictions in one forward pass, matched to ground truth via the Hungarian algorithm during training. DETR's clean formulation influenced the direction of detection research significantly, though its slow convergence (500 epochs vs YOLO's ~100) remains a practical limitation.

```bibtex
@inproceedings{carion2020detr,
  title     = {End-to-End Object Detection with Transformers},
  author    = {Carion, Nicolas and Massa, Francisco and Synnaeve, Gabriel and Usunier, Nicolas and Kirillov, Alexander and Zagoruyko, Sergey},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2020},
  pages     = {213--229}
}
```

---

## Vision-language models

### OWL-ViT — Open-Vocabulary Detection

<CitationBlock
  :number="4"
  authors="Minderer, M., Gritsenko, A., Stone, A., Neumann, M., Weissenborn, D., Dosovitskiy, A., Mahendran, A., Arnab, A., Dehghani, M., Shen, Z., Wang, X., Zhai, X., Kolesnikov, A., and Houlsby, N."
  title="Simple Open-Vocabulary Object Detection with Vision Transformers"
  venue="European Conference on Computer Vision (ECCV)"
  year="2022"
  url="https://arxiv.org/abs/2205.06230"
/>

OWL-ViT applies contrastive pre-training (CLIP-style) to the detection problem. A Vision Transformer backbone processes the image; text query embeddings are projected into the same space. At inference time, the model produces bounding boxes conditioned on arbitrary text queries — enabling zero-shot detection of novel object categories. YOLO-Toys exposes this through the `OWLViTHandler`, which accepts `text_queries` as an `InferenceParams` field.

```bibtex
@inproceedings{minderer2022owlvit,
  title     = {Simple Open-Vocabulary Object Detection with Vision Transformers},
  author    = {Minderer, Matthias and others},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2022}
}
```

### Grounding DINO — Phrase Grounding

<CitationBlock
  :number="5"
  authors="Liu, S., Zeng, Z., Ren, T., Li, F., Zhang, H., Yang, J., Li, C., Yang, J., Su, H., Zhu, J., and Zhang, L."
  title="Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection"
  venue="European Conference on Computer Vision (ECCV)"
  year="2024"
  url="https://arxiv.org/abs/2303.05499"
/>

Grounding DINO fuses DINO (self-supervised ViT) with grounded pre-training to produce an open-set detector that grounds natural language phrases to regions. Unlike OWL-ViT, it supports phrase-level grounding (detecting objects described by multi-word phrases like "a person wearing a red jacket") rather than class-level conditioning. The `GroundingDINOHandler` wraps `transformers.AutoModelForZeroShotObjectDetection`.

```bibtex
@inproceedings{liu2023grounding,
  title     = {Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection},
  author    = {Liu, Shilong and others},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2024}
}
```

### BLIP — Bootstrapped Language-Image Pre-Training

<CitationBlock
  :number="6"
  authors="Li, J., Li, D., Xiong, C., and Hoi, S."
  title="BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation"
  venue="International Conference on Machine Learning (ICML)"
  year="2022"
  url="https://arxiv.org/abs/2201.12086"
/>

BLIP introduces a bootstrapping framework for vision-language pre-training that uses a captioner and filter to reduce noise in web-crawled image-text pairs. The resulting model supports both understanding (visual question answering) and generation (image captioning) in one architecture. YOLO-Toys implements two BLIP surfaces: `BLIPCaptionHandler` for generation and `BLIPVQAHandler` for understanding.

```bibtex
@inproceedings{li2022blip,
  title     = {BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation},
  author    = {Li, Junnan and Li, Dongxu and Xiong, Caiming and Hoi, Steven},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2022}
}
```

---

## Runtime infrastructure

### FastAPI

<CitationBlock
  :number="7"
  authors="Ramírez, S."
  title="FastAPI — Modern web framework for building APIs with Python"
  venue="Open source software"
  year="2019"
  url="https://github.com/tiangolo/fastapi"
/>

```bibtex
@software{ramirez2019fastapi,
  title  = {FastAPI},
  author = {Ramírez, Sebastián},
  year   = {2019},
  url    = {https://github.com/tiangolo/fastapi}
}
```

### PyTorch

<CitationBlock
  :number="8"
  authors="Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga, L., and others."
  title="PyTorch: An Imperative Style, High-Performance Deep Learning Library"
  venue="Advances in Neural Information Processing Systems (NeurIPS)"
  year="2019"
  url="https://arxiv.org/abs/1912.01703"
/>

```bibtex
@inproceedings{paszke2019pytorch,
  title     = {PyTorch: An Imperative Style, High-Performance Deep Learning Library},
  author    = {Paszke, Adam and Gross, Sam and Massa, Francisco and Lerer, Adam and Bradbury, James and others},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2019}
}
```

---

## Adjacent open-source systems

| Project | Design posture | Why compare it | Repository |
|---------|---------------|----------------|------------|
| Triton Inference Server | Maximum throughput, multiple backends | Industry reference for scale-first serving | `triton-inference-server/server` |
| TorchServe | Worker-per-model, packaging-first | PyTorch's official serving approach | `pytorch/serve` |
| BentoML | Packaging and deployment ergonomics | MLOps-oriented serving framework | `bentoml/BentoML` |
| Ultralytics | YOLO-family execution | Upstream library YOLO-Toys depends on | `ultralytics/ultralytics` |
| vLLM | PagedAttention, continuous batching | Reference for memory-efficient LLM serving | `vllm-project/vllm` |
| Ray Serve | Actor-based distributed serving | Distributed vision serving reference | `ray-project/ray` |
| ONNX Runtime | Cross-platform model execution | Potential execution backend for YOLO-Toys | `microsoft/onnxruntime` |
| TensorRT-LLM | NVIDIA GPU-optimized serving | GPU inference optimization reference | `NVIDIA/TensorRT-LLM` |

### Comparative reading guide

**Triton Inference Server** is the industry standard for high-scale model serving: multiple backends (TensorRT, ONNX, PyTorch, TensorFlow), dynamic batching, multi-GPU scheduling, and mature operational tooling. YOLO-Toys is intentionally narrower — it serves only vision models, runs in a single Python process, and optimizes for developer readability over raw throughput. For workloads exceeding hundreds of requests per second, Triton is the right escalation path.

**TorchServe** uses a worker-per-model architecture with a model-archiver packaging format. Model isolation is stronger but inter-process communication adds overhead. YOLO-Toys favors a single-process shared-cache model where hot models benefit from warm GPU memory without worker handoff.

**BentoML** is a model packaging and deployment framework with strong MLOps ergonomics. It abstracts artifact management, deployment pipelines, and service definitions into a deployable unit. YOLO-Toys is more opinionated around heterogeneous vision inference — the handler and registry system provides a built-in architecture rather than a blank deployment surface.

**vLLM** is included despite being LLM-focused because its PagedAttention memory management and continuous batching solve problems structurally similar to YOLO-Toys' cache pressure concerns. The vision serving community lacks an equivalent memory-management innovation; the YOLO-Toys LRU+TTL+memory-pressure cache is a practical approximation.

**RT-DETR** (Baidu, 2023) and **DINO** (Zhang et al., 2022) are notable omissions from the current runtime. They represent the state-of-the-art in real-time transformer detection. Adding RT-DETR would require a new `ModelCategory.HF_RTDETR` entry, a handler extending `DETRHandler`, and registration in the model registry. This is the intended extension path for contributors.

---

## Design pattern references

The YOLO-Toys architecture draws deliberately on established software engineering patterns:

| Pattern | Where it appears in YOLO-Toys | Reference |
|---------|------------------------------|-----------|
| **Strategy / Template Method** | `BaseHandler` + family-specific subclasses | Gamma et al., *Design Patterns* (1994) |
| **Registry** | `HandlerRegistry` — category-to-handler mapping | Fowler, *Patterns of Enterprise Application Architecture* (2002) |
| **Deep Module** | `LoadedModel` — hides processor complexity behind `infer()` | Ousterhout, *A Philosophy of Software Design* (2018) |
| **Adapter** | `SettingsModelManagerConfig` — Pydantic settings → protocol | Gamma et al., *Design Patterns* (1994) |
| **Protocol / Interface Segregation** | `ModelManagerConfig` — structural subtyping via PEP 544 | Van Rossum, PEP 544 — Protocols for Python (2017) |
| **Observer / MutationObserver** | Dark mode detection in theme system | Browser API; implicit in VitePress theme |

The intersection of these patterns is deliberate: YOLO-Toys uses Strategy to localize model-specific behavior, Registry to make dispatch deterministic and introspectable, and Deep Module to present a simple `infer()` surface regardless of underlying complexity.

---

## What to read next

- [Evolution](/en/research/evolution) — how these influences shaped the runtime's actual design decisions
- [Comparisons](/en/reference/comparisons) — decision matrix when choosing a serving system
- [Handler Pattern](/en/academy/handler-pattern) — the design pattern deep dive
- [Architecture Overview](/en/architecture/overview) — the full runtime model
