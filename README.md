# YOLO-Toys

> 把 YOLOv8、DETR、OWL-ViT、Grounding DINO、BLIP 统一到 FastAPI + WebSocket 接口下的多模型视觉推理服务。

## 快速开始

### Docker

```bash
docker run -p 8000:8000 ghcr.io/vibe-knight/yolo-toys:latest
```

打开 <http://localhost:8000>。

### 本地开发

```bash
git clone https://github.com/vibe-knight/yolo-toys.git
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

## 开发命令

```bash
make lint       # 代码检查
make format     # 自动格式化
make test       # 测试
make typecheck  # 类型检查
```
