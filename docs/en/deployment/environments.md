# Environment Variables Reference

Complete reference for all configuration options.

---

## 📋 Quick Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Server port |
| `MODEL_NAME` | `yolov8n.pt` | Default model |
| `DEVICE` | `auto` | Inference device |
| `CONF_THRESHOLD` | `0.25` | Detection confidence |
| `IOU_THRESHOLD` | `0.45` | NMS IoU threshold |
| `MAX_DET` | `300` | Max detections |
| `MAX_CONCURRENCY` | `4` | Concurrent requests |

---

## 🔧 Server Configuration

### PORT

```bash
PORT=8080
```

### ALLOW_ORIGINS

```bash
ALLOW_ORIGINS=https://yourdomain.com
ALLOW_ORIGINS=*  # Allow all (development only)
```

---

## 🤖 Model Configuration

### MODEL_NAME

```bash
MODEL_NAME=yolov8n.pt          # Fastest
MODEL_NAME=yolov8s.pt          # Balanced
MODEL_NAME=facebook/detr-resnet-50  # DETR
```

### DEVICE

```bash
DEVICE=auto     # Auto-detect
DEVICE=cpu      # Force CPU
DEVICE=cuda:0   # Specific GPU
DEVICE=mps      # Apple Silicon
```

---

## ⚡ Performance Configuration

### MAX_CONCURRENCY

```bash
MAX_CONCURRENCY=4   # Default
MAX_CONCURRENCY=8   # High-throughput
```

---

## 📝 Example .env File

### Development

```bash
PORT=8000
ALLOW_ORIGINS=*
MODEL_NAME=yolov8n.pt
DEVICE=auto
LOG_LEVEL=debug
```

### Production

```bash
PORT=8000
ALLOW_ORIGINS=https://yourdomain.com
MODEL_NAME=yolov8s.pt
DEVICE=auto
MAX_CONCURRENCY=4
LOG_LEVEL=info
```

---

## 🔗 Related Documentation

- [Docker Deployment](./docker) — Container deployment
- [Architecture](../architecture/overview) — System design
