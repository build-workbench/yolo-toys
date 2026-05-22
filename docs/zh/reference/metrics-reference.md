---
title: Prometheus 指标参考
---

# Prometheus 指标参考

YOLO-Toys 暴露全面的 Prometheus 指标以实现可观测性。所有指标都可在 `/metrics` 端点获取。

## 应用指标

### `yolo_toys_info`

应用元数据。

```
# TYPE yolo_toys_info gauge
yolo_toys_info{version="3.2.0",python="3.11"} 1
```

| 标签 | 描述 |
|------|------|
| `version` | 应用版本 |
| `python` | Python 版本 |

## 推理指标

### `yolo_inference_requests_total`

推理请求总数计数器。

```
# TYPE yolo_inference_requests_total counter
yolo_inference_requests_total{model="yolov8n.pt",task="detect",status="success"} 1523
yolo_inference_requests_total{model="yolov8n.pt",task="detect",status="error"} 2
```

| 标签 | 取值 |
|------|------|
| `model` | 模型标识符 |
| `task` | detect, segment, pose, caption, vqa |
| `status` | success, error |

### `yolo_inference_latency_seconds`

推理延迟直方图。

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

**直方图桶**：10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s, 10s

### `yolo_inference_input_size_bytes`

输入图像大小直方图。

```
# TYPE yolo_inference_input_size_bytes histogram
yolo_inference_input_size_bytes_bucket{le="100000"} 234
yolo_inference_input_size_bytes_bucket{le="500000"} 892
yolo_inference_input_size_bytes_bucket{le="1000000"} 1456
```

## 模型指标

### `yolo_model_load_time_seconds`

模型加载时间测量值。

```
# TYPE yolo_model_load_time_seconds gauge
yolo_model_load_time_seconds{model_id="yolov8n.pt"} 0.42
yolo_model_load_time_seconds{model_id="yolov8x.pt"} 3.21
```

### `yolo_model_cache_size`

当前缓存大小。

```
# TYPE yolo_model_cache_size gauge
yolo_model_cache_size 5
```

### `yolo_model_cache_max_size`

最大缓存大小。

```
# TYPE yolo_model_cache_max_size gauge
yolo_model_cache_max_size 10
```

### `yolo_model_memory_usage_bytes`

模型内存使用。

```
# TYPE yolo_model_memory_usage_bytes gauge
yolo_model_memory_usage_bytes{model_id="yolov8n.pt"} 64000000
```

### `yolo_model_cache_evictions_total`

缓存驱逐计数器。

```
# TYPE yolo_model_cache_evictions_total counter
yolo_model_cache_evictions_total{reason="lru"} 12
yolo_model_cache_evictions_total{reason="ttl"} 5
```

| 原因 | 描述 |
|------|------|
| `lru` | 因内存压力而驱逐 |
| `ttl` | 因 TTL 过期而驱逐 |

## WebSocket 指标

### `yolo_websocket_connections`

活跃 WebSocket 连接数。

```
# TYPE yolo_websocket_connections gauge
yolo_websocket_connections 3
```

### `yolo_websocket_messages_total`

WebSocket 消息计数器。

```
# TYPE yolo_websocket_messages_total counter
yolo_websocket_messages_total{message_type="result",direction="outbound"} 4523
yolo_websocket_messages_total{message_type="config",direction="inbound"} 12
```

| 方向 | 描述 |
|------|------|
| `inbound` | 客户端 → 服务器 |
| `outbound` | 服务器 → 客户端 |

## HTTP 指标

### `yolo_http_request_duration_seconds`

HTTP 请求持续时间直方图。

```
# TYPE yolo_http_request_duration_seconds histogram
yolo_http_request_duration_seconds_bucket{method="POST",endpoint="/infer",status_code="200",le="0.1"} 892
```

| 标签 | 取值 |
|------|------|
| `method` | GET, POST |
| `endpoint` | /health, /infer, /caption, /vqa 等 |
| `status_code` | 200, 400, 404, 500 等 |

## 系统指标

### `yolo_system_memory_used_bytes`

系统内存使用。

```
# TYPE yolo_system_memory_used_bytes gauge
yolo_system_memory_used_bytes 4200000000
```

### `yolo_system_memory_total_bytes`

系统总内存。

```
# TYPE yolo_system_memory_total_bytes gauge
yolo_system_memory_total_bytes 16000000000
```

### `yolo_system_memory_percent`

内存使用百分比。

```
# TYPE yolo_system_memory_percent gauge
yolo_system_memory_percent 0.26
```

### `yolo_system_gpu_memory_used_bytes`

GPU 内存使用（如果 CUDA 可用）。

```
# TYPE yolo_system_gpu_memory_used_bytes gauge
yolo_system_gpu_memory_used_bytes{device="0"} 2000000000
```

## Grafana 仪表板

### 示例 PromQL 查询

**推理速率**

```promql
rate(yolo_inference_requests_total{status="success"}[5m])
```

**P95 延迟**

```promql
histogram_quantile(0.95,
  rate(yolo_inference_latency_seconds_bucket[5m])
)
```

**错误率**

```promql
sum(rate(yolo_inference_requests_total{status="error"}[5m]))
/
sum(rate(yolo_inference_requests_total[5m]))
```

**缓存命中率**

```promql
rate(yolo_model_cache_hits_total[5m])
/
(rate(yolo_model_cache_hits_total[5m]) + rate(yolo_model_cache_misses_total[5m]))
```

**内存压力**

```promql
yolo_system_memory_percent > 0.8
```

### 告警规则

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
          summary: 检测到高错误率

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            rate(yolo_inference_latency_seconds_bucket[5m])
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: P95 延迟超过 1 秒

      - alert: MemoryPressure
        expr: yolo_system_memory_percent > 0.85
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: 内存使用超过 85%
```

## 推荐阅读

<CrossReference href="/zh/deployment/monitoring" section="部署" label="监控设置" />
<CrossReference href="/zh/reference/configuration-reference" section="参考" label="配置参考" />
