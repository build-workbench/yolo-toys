---
title: 参考文献与相关工作
---

# 参考文献与相关工作

YOLO-Toys 处在实用服务化与上游模型研究的交汇点。本页承担两项任务：

1. 保存运行时依赖的模型家族与框架的引用材料
2. 将本项目置于解决相关服务化问题的相邻开源系统之中进行定位

## 核心文献索引

| 领域 | 主要工作 | 在此处的意义 |
|------|-------------|---------------------|
| YOLO 家族 | Redmon 等 (CVPR 2016)；Jocher 等 (Ultralytics 2023) | 确立了主导运行时吞吐量优化路径的单阶段检测谱系 |
| Transformer 检测 | DETR, Carion 等 (ECCV 2020) | 确立了运行时中基于 Transformer 的检测谱系 |
| 开放词汇检测 | OWL-ViT, Minderer 等 (ECCV 2022) | 奠定了文本条件检测支持的基础 |
| Grounded Detection | Grounding DINO, Liu 等 (ECCV 2024) | 支持基于短语的目标检测 |
| 视觉语言预训练 | BLIP, Li 等 (ICML 2023) | 支撑图像描述与视觉问答接口 |
| 服务框架 | FastAPI, Ramalho 等 (2019)；PyTorch, Paszke 等 (NeurIPS 2019) | 提供运行时底层与模型生态 |
| 异步 Web 框架 | Starlette, Archer (2018) | FastAPI 所依赖的 ASGI 基础 |
| 配置模式 | Pydantic Settings, Colucci 等 (2022) | 实现类型安全的环境变量读取 |

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

## 值得与 YOLO-Toys 对照阅读的相关开源项目

| 项目 | 对照理由 | GitHub |
|---------|---------------|--------|
| Triton Inference Server | 理解规模优先、性能优先的服务假设 | `triton-inference-server/server` |
| TorchServe | 理解基于 worker 的 PyTorch 服务模式 | `pytorch/serve` |
| BentoML | 理解打包与部署工作流的不同侧重 | `bentoml/BentoML` |
| Ultralytics | 理解 YOLO 家族的上游执行模型 | `ultralytics/ultralytics` |
| vLLM | 参考基于 PagedAttention 的 LLM 服务设计 | `vllm-project/vllm` |
| Ray Serve | 理解基于 actor 的分布式服务模式 | `ray-project/ray` |
| ONNX Runtime | 理解跨平台模型加速与部署 | `microsoft/onnxruntime` |
| TensorRT | 理解 NVIDIA GPU 优化推理加速 | `NVIDIA/TensorRT` |

### 对照阅读指南

**Triton Inference Server** 是高规模模型服务的行业标准。它支持多种后端（TensorRT、ONNX、PyTorch、TensorFlow）、动态批处理和多 GPU 调度。YOLO-Toys 有意做得更窄：仅服务视觉模型，使用单一 Python 进程，并优化开发者可读性而非吞吐量最大化。

**TorchServe** 是 PyTorch 官方的服务解决方案。它采用每模型一个 worker 的架构，并带有模型归档器打包格式。YOLO-Toys 的区别在于将所有处理器保留在单一运行时进程中，并共享缓存，避免了 TorchServe 产生的跨进程通信开销。

**BentoML** 是一个模型服务框架，在打包与部署的易用性方面表现出色。它将模型产物与服务定义抽象为可部署单元。YOLO-Toys 更为专一：它不试图成为通用服务框架，而是一个专为异构视觉推理打造的运行时。

**vLLM** 虽聚焦于 LLM，但其 PagedAttention 内存管理与连续批处理是视觉服务领域值得参考的研究方向。视觉服务社区尚未产生能与 vLLM 内存效率相媲美的方案。

## 设计模式参考

YOLO-Toys 的架构借鉴了成熟的软件工程模式：

| 模式 | 出现位置 | 参考 |
|---------|-----------------|-----------|
| 策略 / 模板方法 | `BaseHandler` + 子类 | Gamma 等, *Design Patterns* (1994) |
| 注册表 | `HandlerRegistry` | Fowler, *Patterns of Enterprise Application Architecture* (2002) |
| 深模块 | `LoadedModel` 隐藏 `processor` | Martin, *Clean Architecture* (2017) |
| 协议 / 接口隔离 | `ModelManagerConfig` 协议 | PEP 544 — Protocols (2017) |
| 适配器 | `SettingsModelManagerConfig` | Gamma 等, *Design Patterns* (1994) |

## 接下来阅读什么

- [演进](/en/research/evolution) 了解这些影响如何塑造了运行时的设计决策
- [对比](/en/reference/comparisons) 选择服务系统时的决策矩阵
