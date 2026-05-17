---
title: Configuration Reference
---

# Configuration Reference

YOLO-Toys uses environment variables for all configuration, following the [12-Factor App](https://12factor.net/config) methodology. Configuration is managed through Pydantic Settings for type safety and validation.

## Core Server Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PORT` | `int` | `8000` | Server port |
| `HOST` | `str` | `0.0.0.0` | Bind address |
| `LOG_LEVEL` | `str` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `WORKERS` | `int` | `1` | Number of worker processes |

### Example

```bash
export PORT=8080
export LOG_LEVEL=DEBUG
```

## Model Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MODEL_NAME` | `str` | `yolov8s.pt` | Default model for `/infer` |
| `DEVICE` | `str` | `auto` | Device (auto, cpu, cuda, mps) |
| `SKIP_WARMUP` | `bool` | `false` | Skip model warmup on startup |

### Device Selection Logic

```
auto → CUDA if available → MPS if available → CPU
```

## Inference Parameters

| Variable | Type | Default | Range | Description |
|----------|------|---------|-------|-------------|
| `CONF_THRESHOLD` | `float` | `0.25` | 0.0-1.0 | Confidence threshold |
| `IOU_THRESHOLD` | `float` | `0.45` | 0.0-1.0 | IoU threshold for NMS |
| `MAX_DET` | `int` | `300` | 1-1000 | Maximum detections per image |
| `IMGSZ` | `int` | `640` | 32-4096 | Inference image size |
| `HALF` | `bool` | `false` | - | Use FP16 inference |

### Per-Request Override

```json
{
  "model": "yolov8n.pt",
  "image": "<base64>",
  "conf": 0.5,
  "iou": 0.4,
  "max_det": 100
}
```

## Cache Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MODEL_CACHE_MAXSIZE` | `int` | `10` | Maximum cached models |
| `MODEL_CACHE_TTL` | `int` | `3600` | Cache TTL in seconds |
| `MODEL_MEMORY_THRESHOLD` | `float` | `0.85` | Memory threshold (0-1) |

### Cache Behavior

```
Request → Cache Check
         ├─ Hit  → Return cached model
         └─ Miss → Check memory
                   ├─ Under threshold → Load model
                   └─ Over threshold  → Evict LRU → Load model
```

## Concurrency Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MAX_CONCURRENCY` | `int` | `4` | Max concurrent inferences |
| `REQUEST_TIMEOUT` | `int` | `60` | Request timeout in seconds |

### Semaphore-Based Control

```python
# Internally managed
self._semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

async def infer_with_limit(...):
    async with self._semaphore:
        return await self._infer_internal(...)
```

## Upload Limits

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MAX_UPLOAD_MB` | `int` | `10` | Max upload size in MB |

### Enforced At

1. FastAPI request size limit
2. Image validation middleware
3. Memory guard before processing

## Security Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `RATE_LIMIT_RPM` | `int` | `60` | Requests per minute per IP |
| `CORS_ORIGINS` | `str` | `""` | Comma-separated CORS origins |

### CORS Configuration

```bash
# Single origin
export CORS_ORIGINS="https://example.com"

# Multiple origins
export CORS_ORIGINS="https://example.com,https://api.example.com"

# Allow all (development only!)
export CORS_ORIGINS="*"
```

## BLIP-Specific Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `BLIP_MAX_TOKENS` | `int` | `20` | Max tokens for captioning |
| `BLIP_VQA_MAX_TOKENS` | `int` | `50` | Max tokens for VQA |

## Monitoring Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `METRICS_ENABLED` | `bool` | `true` | Enable Prometheus metrics |
| `METRICS_PORT` | `int` | `9090` | Metrics server port |

### Prometheus Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/metrics` | Prometheus metrics |
| `/health` | Health check + system info |
| `/system/stats` | Detailed system statistics |
| `/system/cache/clear` | Clear model cache (POST) |

## Environment File Example

Create a `.env` file in your project root:

```env
# Server
PORT=8000
LOG_LEVEL=INFO

# Model
MODEL_NAME=yolov8s.pt
DEVICE=auto

# Inference
CONF_THRESHOLD=0.25
IOU_THRESHOLD=0.45
MAX_DET=300

# Cache
MODEL_CACHE_MAXSIZE=10
MODEL_CACHE_TTL=3600
MODEL_MEMORY_THRESHOLD=0.85

# Concurrency
MAX_CONCURRENCY=4
REQUEST_TIMEOUT=60

# Upload
MAX_UPLOAD_MB=10

# Security
RATE_LIMIT_RPM=60
CORS_ORIGINS=https://example.com

# Monitoring
METRICS_ENABLED=true
```

## Configuration in Docker

### Dockerfile

```dockerfile
ENV PORT=8000
ENV DEVICE=auto
ENV MODEL_NAME=yolov8s.pt
```

### docker-compose.yml

```yaml
services:
  yolo-toys:
    image: yolo-toys:latest
    environment:
      - PORT=8000
      - DEVICE=cuda
      - MODEL_NAME=yolov8x.pt
      - CONF_THRESHOLD=0.3
    ports:
      - "8000:8000"
```

## Configuration in Kubernetes

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: yolo-toys-config
data:
  PORT: "8000"
  DEVICE: "cuda"
  MODEL_NAME: "yolov8s.pt"
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: yolo-toys
          envFrom:
            - configMapRef:
                name: yolo-toys-config
```

## Validation

All settings are validated at startup:

```python
class AppSettings(BaseSettings):
    conf_threshold: float = 0.25

    @validator("conf_threshold")
    def validate_conf(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("conf_threshold must be in [0, 1]")
        return v
```

Invalid configuration will prevent startup with a clear error message.

## What to Read Next

<CrossReference href="/en/deployment/docker" section="Deployment" label="Docker Deployment" />
<CrossReference href="/en/reference/benchmarks" section="Reference" label="Performance Benchmarks" />
