**English** | [中文](#chinese)

<a id="top"></a>

# YOLO-Toys

> A multi-model visual inference service that unifies YOLOv8, DETR, OWL-ViT, Grounding DINO, and BLIP behind FastAPI + WebSocket interfaces.

![YOLO-Toys interface preview](docs/screenshot.png)

## Getting Started

### Docker

```bash
docker run -p 8000:8000 ghcr.io/build-workbench/yolo-toys:latest
```

Open <http://localhost:8000>.

### GPU

The default image runs on CPU. For NVIDIA GPUs, build the CUDA image and set `DEVICE=cuda:0`:

```bash
docker build -f deployments/docker/Dockerfile.cuda -t yolo-toys:cuda .
docker run --gpus all -p 8000:8000 -e DEVICE=cuda:0 yolo-toys:cuda
```

`deployments/docker/docker-compose.yml` ships a commented-out `app-gpu` service and CPU memory limits you can adapt. Model weights are downloaded from Hugging Face on first use and cached in the `model-cache` volume.

### Local Development

```bash
git clone https://github.com/build-workbench/yolo-toys.git
cd yolo-toys
bash scripts/dev.sh setup
. .venv/bin/activate
make run
```

## API

| Endpoint | Purpose |
| --- | --- |
| `POST /infer` | Detection / segmentation / pose / open-vocabulary inference |
| `POST /caption` | BLIP image captioning |
| `POST /vqa` | BLIP visual question answering |
| `GET /models` | Model list |
| `GET /labels` | Class labels |
| `WS /ws` | Real-time streaming inference |
| `GET /metrics` | Prometheus metrics |
| `GET /health` | Health check |

## Supported Models

| Family | Examples | Tasks |
| --- | --- | --- |
| YOLOv8 | `yolov8n.pt`, `yolov8n-seg.pt`, `yolov8n-pose.pt` | detect / segment / pose |
| DETR | `facebook/detr-resnet-50` | detect |
| OWL-ViT / Grounding DINO | `google/owlvit-base-patch32` | zero-shot detection |
| BLIP | `Salesforce/blip-image-captioning-base`, `Salesforce/blip-vqa-base` | caption / vqa |

## Hardware Requirements (Self-Hosting)

Approximate fp32 estimates, including the ~1 GB PyTorch runtime baseline. Weights are downloaded on first use; multiple models stay cached (`MODEL_CACHE_MAXSIZE`, default 10), so budget RAM/VRAM for the sum of the models you actually use.

| Model | Weights download | Recommended RAM (CPU) | VRAM (GPU) |
| --- | --- | --- | --- |
| `yolov8n.pt` (detect / seg / pose) | ~10 MB | ~2 GB | ~2 GB |
| `yolov8s.pt` (default) | ~25 MB | ~2 GB | ~2 GB |
| `facebook/detr-resnet-50` | ~170 MB | ~2.5 GB | ~2.5 GB |
| `google/owlvit-base-patch32` (zero-shot) | ~600 MB | ~3 GB | ~3 GB |
| Grounding DINO (tiny) | ~700 MB | ~4 GB | ~4 GB |
| `Salesforce/blip-image-captioning-base` | ~1 GB | ~3 GB | ~3 GB |
| `Salesforce/blip-vqa-base` | ~1.5 GB | ~4 GB | ~4 GB |

Practical guidance:

- **CPU-only is fine for the YOLO/BLIP defaults** (≥4 GB RAM); expect roughly a second per image at 640 px. OWL-ViT and Grounding DINO are noticeably slower on CPU — a GPU is strongly recommended for them.
- **Any 4 GB+ CUDA GPU covers the default model set**; multi-model workloads or larger batch/stream inference benefit from 6-8 GB.
- The service enforces `MAX_UPLOAD_MB` and `MAX_CONCURRENCY`; peak memory scales with concurrency × active model size. Keep `MAX_CONCURRENCY` low on small hosts.

## Development Commands

```bash
make lint       # 代码检查
make format     # 自动格式化
make test       # 测试
make typecheck  # 类型检查
```

## License

[MIT](LICENSE)

---

<a id="chinese"></a>
[English](#top) | **中文**

# YOLO-Toys

> 把 YOLOv8、DETR、OWL-ViT、Grounding DINO、BLIP 统一到 FastAPI + WebSocket 接口下的多模型视觉推理服务。

![YOLO-Toys 界面预览](docs/screenshot.png)

## 快速开始

### Docker

```bash
docker run -p 8000:8000 ghcr.io/build-workbench/yolo-toys:latest
```

打开 <http://localhost:8000>。

### GPU

默认镜像跑 CPU。有 NVIDIA 显卡时，构建 CUDA 镜像并设置 `DEVICE=cuda:0`：

```bash
docker build -f deployments/docker/Dockerfile.cuda -t yolo-toys:cuda .
docker run --gpus all -p 8000:8000 -e DEVICE=cuda:0 yolo-toys:cuda
```

`deployments/docker/docker-compose.yml` 内置了注释掉的 `app-gpu` 服务与 CPU 内存限制，按需打开调整。模型权重首次使用时从 Hugging Face 下载，缓存在 `model-cache` 卷中。

### 本地开发

```bash
git clone https://github.com/build-workbench/yolo-toys.git
cd yolo-toys
bash scripts/dev.sh setup
. .venv/bin/activate
make run
```

## API

| 入口 | 作用 |
| --- | --- |
| `POST /infer` | 检测 / 分割 / 姿态 / 开放词汇推理 |
| `POST /caption` | BLIP 图像描述 |
| `POST /vqa` | BLIP 视觉问答 |
| `GET /models` | 模型列表 |
| `GET /labels` | 类别标签 |
| `WS /ws` | 实时流式推理 |
| `GET /metrics` | Prometheus 指标 |
| `GET /health` | 健康检查 |

## 支持的模型

| 家族 | 示例 | 任务 |
| --- | --- | --- |
| YOLOv8 | `yolov8n.pt`、`yolov8n-seg.pt`、`yolov8n-pose.pt` | detect / segment / pose |
| DETR | `facebook/detr-resnet-50` | detect |
| OWL-ViT / Grounding DINO | `google/owlvit-base-patch32` | 零样本检测 |
| BLIP | `Salesforce/blip-image-captioning-base`、`Salesforce/blip-vqa-base` | caption / vqa |

## 硬件需求（自部署）

以下为 fp32 的近似估算，已包含约 1 GB 的 PyTorch 运行时基线。权重首次使用时下载；已加载的模型会驻留缓存（`MODEL_CACHE_MAXSIZE`，默认 10 个），内存/显存请按"实际会用到的模型之和"预留。

| 模型 | 权重下载体积 | 内存（CPU 推理） | 显存（GPU 推理） |
| --- | --- | --- | --- |
| `yolov8n.pt`（detect / seg / pose） | 约 10 MB | 约 2 GB | 约 2 GB |
| `yolov8s.pt`（默认） | 约 25 MB | 约 2 GB | 约 2 GB |
| `facebook/detr-resnet-50` | 约 170 MB | 约 2.5 GB | 约 2.5 GB |
| `google/owlvit-base-patch32`（零样本） | 约 600 MB | 约 3 GB | 约 3 GB |
| Grounding DINO（tiny） | 约 700 MB | 约 4 GB | 约 4 GB |
| `Salesforce/blip-image-captioning-base` | 约 1 GB | 约 3 GB | 约 3 GB |
| `Salesforce/blip-vqa-base` | 约 1.5 GB | 约 4 GB | 约 4 GB |

实操建议：

- **只用 YOLO/BLIP 默认模型时 CPU 完全够用**（内存 ≥4 GB）；640 px 输入下单张图约一秒级。OWL-ViT 和 Grounding DINO 在 CPU 上明显偏慢——这两个强烈建议上 GPU。
- **任何 4 GB 以上显存的 CUDA 显卡都能覆盖默认模型组合**；多模型并存或批量/流式推理建议 6-8 GB。
- 服务受 `MAX_UPLOAD_MB` 与 `MAX_CONCURRENCY` 约束；峰值内存约为"并发数 × 所用模型体积"，小机器请调低 `MAX_CONCURRENCY`。

## 开发命令

```bash
make lint       # 代码检查
make format     # 自动格式化
make test       # 测试
make typecheck  # 类型检查
```

## 开源协议

[MIT](LICENSE)
