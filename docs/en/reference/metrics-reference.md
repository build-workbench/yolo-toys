---
title: Prometheus Metrics Reference
---

# Prometheus Metrics Reference

YOLO-Toys exposes comprehensive Prometheus metrics for observability. All metrics are available at the `/metrics` endpoint.

## Application Metrics

### `yolo_toys_info`

Application metadata.

```
# TYPE yolo_toys_info gauge
yolo_toys_info{version="3.2.0",python="3.11"} 1
```

| Label | Description |
|-------|-------------|
| `version` | Application version |
| `python` | Python version |

## Inference Metrics

### `yolo_inference_requests_total`

Total inference requests counter.

```
# TYPE yolo_inference_requests_total counter
yolo_inference_requests_total{model="yolov8n.pt",task="detect",status="success"} 1523
yolo_inference_requests_total{model="yolov8n.pt",task="detect",status="error"} 2
```

| Label | Values |
|-------|--------|
| `model` | Model identifier |
| `task` | detect, segment, pose, caption, vqa |
| `status` | success, error |

### `yolo_inference_latency_seconds`

Inference latency histogram.

```
# TYPE yolo_inference_latency_seconds histogram
yolo_inference_latency_seconds_bucket{model="yolov8n.pt",task="detect",le="0.01"} 45
yolo_inference_latency_seconds_bucket{model="yolov8n.pt",task="detect",le="0.025"} 312
yolo_inference_latency_seconds_bucket{model="yolov8n.pt",task="detect",le="0.05"} 892
yolo_inference_latency_seconds_bucket{model="yolov8n.pt",task="detect",le="0.1"} 1456
yolo_inference_latency_seconds_bucket{model="yolov8n.pt",task="detect",le="+Inf"} 1523
yolo_inference_latency_seconds_sum{model="yolov8n.pt",task="detect"} 45.23
yolo_inference_latency_seconds_count{model="yolov8n.pt",task="detect"} 1523
```

**Histogram Buckets**: 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s, 10s

### `yolo_inference_input_size_bytes`

Input image size histogram.

```
# TYPE yolo_inference_input_size_bytes histogram
yolo_inference_input_size_bytes_bucket{le="100000"} 234
yolo_inference_input_size_bytes_bucket{le="500000"} 892
yolo_inference_input_size_bytes_bucket{le="1000000"} 1456
```

## Model Metrics

### `yolo_model_load_time_seconds`

Model load time gauge.

```
# TYPE yolo_model_load_time_seconds gauge
yolo_model_load_time_seconds{model_id="yolov8n.pt"} 0.42
yolo_model_load_time_seconds{model_id="yolov8x.pt"} 3.21
```

### `yolo_model_cache_size`

Current cache size.

```
# TYPE yolo_model_cache_size gauge
yolo_model_cache_size 5
```

### `yolo_model_cache_max_size`

Maximum cache size.

```
# TYPE yolo_model_cache_max_size gauge
yolo_model_cache_max_size 10
```

### `yolo_model_memory_usage_bytes`

Model memory usage.

```
# TYPE yolo_model_memory_usage_bytes gauge
yolo_model_memory_usage_bytes{model_id="yolov8n.pt"} 64000000
```

### `yolo_model_cache_evictions_total`

Cache eviction counter.

```
# TYPE yolo_model_cache_evictions_total counter
yolo_model_cache_evictions_total{reason="lru"} 12
yolo_model_cache_evictions_total{reason="ttl"} 5
```

| Reason | Description |
|--------|-------------|
| `lru` | Evicted due to memory pressure |
| `ttl` | Evicted due to TTL expiry |

## WebSocket Metrics

### `yolo_websocket_connections`

Active WebSocket connections.

```
# TYPE yolo_websocket_connections gauge
yolo_websocket_connections 3
```

### `yolo_websocket_messages_total`

WebSocket message counter.

```
# TYPE yolo_websocket_messages_total counter
yolo_websocket_messages_total{message_type="result",direction="outbound"} 4523
yolo_websocket_messages_total{message_type="config",direction="inbound"} 12
```

| Direction | Description |
|-----------|-------------|
| `inbound` | Client → Server |
| `outbound` | Server → Client |

## HTTP Metrics

### `yolo_http_request_duration_seconds`

HTTP request duration histogram.

```
# TYPE yolo_http_request_duration_seconds histogram
yolo_http_request_duration_seconds_bucket{method="POST",endpoint="/infer",status_code="200",le="0.1"} 892
```

| Label | Values |
|-------|--------|
| `method` | GET, POST |
| `endpoint` | /health, /infer, /caption, /vqa, etc. |
| `status_code` | 200, 400, 404, 500, etc. |

## System Metrics

### `yolo_system_memory_used_bytes`

System memory usage.

```
# TYPE yolo_system_memory_used_bytes gauge
yolo_system_memory_used_bytes 4200000000
```

### `yolo_system_memory_total_bytes`

Total system memory.

```
# TYPE yolo_system_memory_total_bytes gauge
yolo_system_memory_total_bytes 16000000000
```

### `yolo_system_memory_percent`

Memory usage percentage.

```
# TYPE yolo_system_memory_percent gauge
yolo_system_memory_percent 0.26
```

### `yolo_system_gpu_memory_used_bytes`

GPU memory usage (if CUDA available).

```
# TYPE yolo_system_gpu_memory_used_bytes gauge
yolo_system_gpu_memory_used_bytes{device="0"} 2000000000
```

## Grafana Dashboard

### Example PromQL Queries

**Inference Rate**

```promql
rate(yolo_inference_requests_total{status="success"}[5m])
```

**P95 Latency**

```promql
histogram_quantile(0.95,
  rate(yolo_inference_latency_seconds_bucket[5m])
)
```

**Error Rate**

```promql
sum(rate(yolo_inference_requests_total{status="error"}[5m]))
/
sum(rate(yolo_inference_requests_total[5m]))
```

**Cache Hit Rate**

```promql
rate(yolo_model_cache_hits_total[5m])
/
(rate(yolo_model_cache_hits_total[5m]) + rate(yolo_model_cache_misses_total[5m]))
```

**Memory Pressure**

```promql
yolo_system_memory_percent > 0.8
```

### Alerting Rules

```yaml
groups:
  - name: yolo-toys
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(yolo_inference_requests_total{status="error"}[5m]))
          /
          sum(rate(yolo_inference_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High error rate detected

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            rate(yolo_inference_latency_seconds_bucket[5m])
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: P95 latency exceeds 1 second

      - alert: MemoryPressure
        expr: yolo_system_memory_percent > 0.85
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: Memory usage exceeds 85%
```

## What to Read Next

<CrossReference href="/en/deployment/monitoring" section="Deployment" label="Monitoring Setup" />
<CrossReference href="/en/reference/configuration-reference" section="Reference" label="Configuration Reference" />
