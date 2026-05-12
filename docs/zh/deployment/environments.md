# 环境变量参考

所有配置选项的完整参考。

---

## 📋 快速参考

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `PORT` | `8000` | 服务器端口 |
| `MODEL_NAME` | `yolov8n.pt` | 默认模型 |
| `DEVICE` | `auto` | 推理设备 |
| `CONF_THRESHOLD` | `0.25` | 检测置信度 |
| `IOU_THRESHOLD` | `0.45` | NMS IoU 阈值 |
| `MAX_DET` | `300` | 最大检测数 |
| `MAX_CONCURRENCY` | `4` | 并发请求数 |

---

## 🔧 服务器配置

### PORT

```bash
PORT=8080
```

### ALLOW_ORIGINS

```bash
ALLOW_ORIGINS=https://yourdomain.com
ALLOW_ORIGINS=*  # 允许所有（仅开发）
```

---

## 🤖 模型配置

### MODEL_NAME

```bash
MODEL_NAME=yolov8n.pt          # 最快
MODEL_NAME=yolov8s.pt          # 平衡
MODEL_NAME=facebook/detr-resnet-50  # DETR
```

### DEVICE

```bash
DEVICE=auto     # 自动检测
DEVICE=cpu      # 强制 CPU
DEVICE=cuda:0   # 指定 GPU
DEVICE=mps      # Apple Silicon
```

---

## ⚡ 性能配置

### MAX_CONCURRENCY

```bash
MAX_CONCURRENCY=4   # 默认
MAX_CONCURRENCY=8   # 高吞吐
```

---

## 📝 示例 .env 文件

### 开发环境

```bash
PORT=8000
ALLOW_ORIGINS=*
MODEL_NAME=yolov8n.pt
DEVICE=auto
LOG_LEVEL=debug
```

### 生产环境

```bash
PORT=8000
ALLOW_ORIGINS=https://yourdomain.com
MODEL_NAME=yolov8s.pt
DEVICE=auto
MAX_CONCURRENCY=4
LOG_LEVEL=info
```

---

## 🔗 相关文档

- [Docker 部署](./docker) — 容器部署
- [架构](../architecture/overview) — 系统设计
