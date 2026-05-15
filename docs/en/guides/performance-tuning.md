---
title: Performance Tuning Guide
---

# Performance Tuning Guide

This guide covers techniques to optimize YOLO-Toys performance for your workload.

## Hardware Considerations

### GPU Selection

| GPU | Recommended For | Expected Latency |
|-----|-----------------|------------------|
| NVIDIA T4 | Production inference | 20-50ms (YOLOv8n) |
| NVIDIA V100 | High throughput | 10-20ms |
| NVIDIA A100 | Maximum performance | 5-15ms |
| Apple M1/M2 | Development | 15-30ms |
| CPU | Fallback only | 100-500ms |

### Memory Requirements

| Model | GPU Memory | CPU Memory |
|-------|------------|------------|
| YOLOv8n | ~500 MB | ~200 MB |
| YOLOv8s | ~1 GB | ~400 MB |
| YOLOv8l | ~2 GB | ~800 MB |
| DETR-ResNet50 | ~2 GB | ~600 MB |
| OWL-ViT | ~4 GB | ~1.5 GB |
| BLIP-Large | ~3 GB | ~1 GB |

## Configuration Tuning

### Environment Variables

```bash
# Concurrency
export MAX_CONCURRENCY=8          # Match CPU cores or GPU capacity

# Caching
export MODEL_CACHE_MAXSIZE=20     # More models cached
export MODEL_CACHE_TTL=7200       # 2 hour TTL
export MODEL_MEMORY_THRESHOLD=0.80  # Evict earlier

# Model defaults
export CONF_THRESHOLD=0.3         # Lower = more detections
export IOU_THRESHOLD=0.5          # NMS threshold

# Warmup
export SKIP_WARMUP=false          # Always warmup
export WARMUP_IMAGE_SIZE=640      # Match typical input size
```

### Hardware-Specific Configs

**High-End GPU (A100)**:
```bash
export MAX_CONCURRENCY=16
export MODEL_CACHE_MAXSIZE=30
export DEVICE=cuda:0
```

**Mid-Range GPU (T4)**:
```bash
export MAX_CONCURRENCY=8
export MODEL_CACHE_MAXSIZE=10
export MODEL_MEMORY_THRESHOLD=0.75
```

**CPU Only**:
```bash
export MAX_CONCURRENCY=4
export MODEL_CACHE_MAXSIZE=5
export DEVICE=cpu
```

## Inference Optimization

### Half-Precision (FP16)

Enable FP16 for 2x speedup on supported GPUs:

```bash
# API parameter
POST /infer?half=true

# Or in code
params = InferenceParams(half=True)
```

**Compatibility**: NVIDIA GPUs with FP16 support (Pascal+)

### Input Size

Smaller inputs = faster inference:

```bash
# Reduce inference size
POST /infer?imgsz=320
```

| Size | Relative Speed | Accuracy Impact |
|------|----------------|-----------------|
| 320 | 4x faster | -5% mAP |
| 640 | Baseline | Baseline |
| 1280 | 0.25x | +2% mAP |

### Batch Processing

For multiple images, use WebSocket for connection reuse:

```javascript
// Reuse connection for multiple images
const ws = new WebSocket('ws://host/ws?model=yolov8n.pt');

for (const image of images) {
    ws.send(image);
    // Handle results in onmessage
}
```

## Caching Strategy

### Monitor Cache Efficiency

```bash
# Check cache stats
curl http://localhost:8000/health

# Response includes:
{
  "cache_info": {
    "cache_size": 5,
    "cache_maxsize": 10,
    "cached_models": ["yolov8n.pt", "yolov8s.pt", ...]
  }
}
```

### Prometheus Metrics

```promql
# Cache hit rate
sum(rate(inference_requests_total{status="success"}[5m]))
/
sum(rate(model_load_duration_seconds_count[5m]))

# Memory usage
model_memory_usage_ratio

# Cache evictions (logged, not metric)
```

### Tuning Recommendations

| Scenario | Maxsize | TTL | Threshold |
|----------|---------|-----|-----------|
| Few models, frequent use | 5 | 7200 | 0.90 |
| Many models, varied use | 20 | 3600 | 0.80 |
| Memory constrained | 3 | 1800 | 0.70 |
| Memory abundant | 30 | 14400 | 0.95 |

## Network Optimization

### Image Compression

Reduce upload size:

```python
# Client-side compression
import cv2

def compress_image(image, quality=85):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encoded = cv2.imencode('.jpg', image, encode_param)
    return encoded.tobytes()
```

### Response Compression

GZip middleware is enabled by default:

```bash
export GZIP_MIN_SIZE=500  # Compress responses > 500 bytes
```

### Connection Pooling

Reuse HTTP connections:

```python
import requests

session = requests.Session()

# Reuse connection for multiple requests
for image in images:
    response = session.post(url, files={"file": image})
```

## Benchmarking

### Quick Benchmark

```python
import time
import requests
import numpy as np
import cv2

def benchmark(num_requests=100):
    image = np.zeros((640, 640, 3), dtype=np.uint8)
    _, encoded = cv2.imencode('.jpg', image)

    times = []
    for _ in range(num_requests):
        start = time.time()
        requests.post(
            "http://localhost:8000/infer",
            files={"file": ("test.jpg", encoded.tobytes())}
        )
        times.append(time.time() - start)

    print(f"Mean: {np.mean(times)*1000:.2f}ms")
    print(f"P50: {np.percentile(times, 50)*1000:.2f}ms")
    print(f"P99: {np.percentile(times, 99)*1000:.2f}ms")
```

### Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task

class InferenceUser(HttpUser):
    @task
    def infer(self):
        with open("test_image.jpg", "rb") as f:
            self.client.post(
                "/infer",
                files={"file": f},
                data={"model": "yolov8n.pt"}
            )
```

Run:
```bash
locust -f locustfile.py --host http://localhost:8000
```

## Common Bottlenecks

### 1. Model Loading

**Symptom**: First request slow, subsequent fast.

**Solution**: Warmup at startup (enabled by default).

```bash
export SKIP_WARMUP=false
```

### 2. GPU Memory Exhaustion

**Symptom**: `CUDA out of memory` errors.

**Solutions**:
- Reduce `MODEL_CACHE_MAXSIZE`
- Lower `MODEL_MEMORY_THRESHOLD`
- Use smaller model
- Enable FP16: `half=true`

### 3. CPU Bottleneck

**Symptom**: High CPU usage, low GPU utilization.

**Solutions**:
- Check preprocessing overhead
- Increase `MAX_CONCURRENCY` for parallel processing
- Ensure `DEVICE=cuda` is set

### 4. Network Latency

**Symptom**: High total latency, low inference time.

**Solutions**:
- Compress images before upload
- Use WebSocket for multiple requests
- Deploy closer to clients (edge)

## Monitoring Dashboard

Key metrics to track:

| Metric | Healthy Range | Alert Threshold |
|--------|---------------|-----------------|
| P50 latency | < 50ms | > 100ms |
| P99 latency | < 200ms | > 500ms |
| Error rate | < 0.1% | > 1% |
| Memory usage | < 80% | > 90% |
| Cache hit rate | > 80% | < 50% |

### Grafana Dashboard Example

```json
{
  "panels": [
    {
      "title": "Inference Latency",
      "targets": [{
        "expr": "histogram_quantile(0.50, rate(inference_duration_seconds_bucket[5m]))"
      }]
    },
    {
      "title": "Memory Usage",
      "targets": [{
        "expr": "model_memory_usage_ratio"
      }]
    }
  ]
}
```
