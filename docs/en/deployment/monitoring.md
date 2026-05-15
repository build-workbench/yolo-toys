---
title: Monitoring and Alerting Guide
---

# Monitoring and Alerting Guide

This guide covers setting up monitoring, dashboards, and alerts for YOLO-Toys.

## Metrics Overview

YOLO-Toys exposes Prometheus metrics at the `/metrics` endpoint.

### Application Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `inference_requests_total` | Counter | model, task, status | Total inference requests |
| `inference_duration_seconds` | Histogram | model, task | Inference latency |
| `inference_input_size_bytes` | Histogram | - | Input image sizes |
| `model_load_duration_seconds` | Gauge | model_id | Model loading time |
| `model_cache_size` | Gauge | - | Cached model count |
| `model_memory_usage_ratio` | Gauge | - | Memory usage (0-1) |

### WebSocket Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `websocket_connections_active` | Gauge | - | Active WebSocket connections |
| `websocket_messages_total` | Counter | message_type, direction | WebSocket message count |

### HTTP Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_request_duration_seconds` | Histogram | method, endpoint, status_code | HTTP request latency |

## Prometheus Configuration

### prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'yolo-toys'
    static_configs:
      - targets: ['yolo-toys:8000']
    metrics_path: /metrics
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  yolo-toys:
    image: yolo-toys:latest
    ports:
      - "8000:8000"

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus-data:
  grafana-data:
```

## Grafana Dashboard

### Dashboard JSON

```json
{
  "dashboard": {
    "title": "YOLO-Toys",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(inference_requests_total[5m])) by (model)",
            "legendFormat": "{{model}}"
          }
        ]
      },
      {
        "title": "Latency Distribution",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(inference_duration_seconds_bucket[5m])",
            "format": "heatmap"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "gauge",
        "targets": [
          {
            "expr": "model_memory_usage_ratio * 100"
          }
        ],
        "thresholds": [
          { "value": 70, "color": "yellow" },
          { "value": 85, "color": "red" }
        ]
      },
      {
        "title": "Cache Size",
        "type": "stat",
        "targets": [
          {
            "expr": "model_cache_size"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(inference_requests_total{status=\"error\"}[5m])) / sum(rate(inference_requests_total[5m])) * 100"
          }
        ]
      },
      {
        "title": "WebSocket Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "websocket_connections_active"
          }
        ]
      }
    ]
  }
}
```

## Alert Rules

### alerts.yml

```yaml
groups:
  - name: yolo-toys
    rules:
      # Latency alerts
      - alert: HighLatencyP50
        expr: histogram_quantile(0.50, rate(inference_duration_seconds_bucket[5m])) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High P50 latency"
          description: "P50 latency is {{ $value | humanizeDuration }}"

      - alert: HighLatencyP99
        expr: histogram_quantile(0.99, rate(inference_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High P99 latency"
          description: "P99 latency is {{ $value | humanizeDuration }}"

      # Error rate alerts
      - alert: HighErrorRate
        expr: |
          sum(rate(inference_requests_total{status="error"}[5m]))
          /
          sum(rate(inference_requests_total[5m]))
          > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # Memory alerts
      - alert: MemoryPressure
        expr: model_memory_usage_ratio > 0.85
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Memory pressure detected"
          description: "Memory usage at {{ $value | humanizePercentage }}"

      - alert: MemoryCritical
        expr: model_memory_usage_ratio > 0.95
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Critical memory usage"
          description: "Memory usage at {{ $value | humanizePercentage }}"

      # Cache alerts
      - alert: CacheEvictionFrequent
        expr: rate(model_cache_evictions_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Frequent cache evictions"
          description: "Consider increasing cache size or TTL"

      # Model loading alerts
      - alert: SlowModelLoad
        expr: model_load_duration_seconds > 30
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Slow model loading"
          description: "Model {{ $labels.model_id }} took {{ $value }}s to load"
```

### Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'critical'
    - match:
        severity: warning
      receiver: 'warning'

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://your-webhook/alerts'

  - name: 'critical'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/XXX/YYY/ZZZ'
        channel: '#alerts-critical'
        title: 'YOLO-Toys Alert'
        text: '{{ .Status }}: {{ .CommonAnnotations.summary }}'

  - name: 'warning'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/XXX/YYY/ZZZ'
        channel: '#alerts-warning'
        title: 'YOLO-Toys Warning'
        text: '{{ .Status }}: {{ .CommonAnnotations.summary }}'
```

## Common Queries

### Performance Queries

```promql
# Requests per second
sum(rate(inference_requests_total[5m]))

# Requests by model
sum(rate(inference_requests_total[5m])) by (model)

# P50 latency
histogram_quantile(0.50, rate(inference_duration_seconds_bucket[5m]))

# P99 latency
histogram_quantile(0.99, rate(inference_duration_seconds_bucket[5m]))

# Latency by model
histogram_quantile(0.50, sum(rate(inference_duration_seconds_bucket[5m])) by (model, le))
```

### Error Queries

```promql
# Error rate
sum(rate(inference_requests_total{status="error"}[5m]))
/
sum(rate(inference_requests_total[5m]))

# Errors by model
sum(rate(inference_requests_total{status="error"}[5m])) by (model)

# Error percentage over time
sum(rate(inference_requests_total{status="error"}[1h]))
/
sum(rate(inference_requests_total[1h]))
* 100
```

### Resource Queries

```promql
# Current memory usage
model_memory_usage_ratio

# Cached models
model_cache_size

# Model load times
model_load_duration_seconds

# WebSocket connections
websocket_connections_active
```

## Health Checks

### Basic Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok",
  "version": "3.2.0",
  "device": "cuda:0",
  "default_model": "yolov8s.pt",
  "defaults": {
    "conf": 0.25,
    "iou": 0.45
  }
}
```

### Detailed Health Check Script

```python
import requests
import json

def health_check():
    try:
        # Basic health
        health = requests.get("http://localhost:8000/health").json()

        # Metrics
        metrics = requests.get("http://localhost:8000/metrics").text

        # Parse key metrics
        memory_usage = parse_metric(metrics, "model_memory_usage_ratio")
        cache_size = parse_metric(metrics, "model_cache_size")

        status = {
            "healthy": health["status"] == "ok",
            "device": health["device"],
            "memory_usage": memory_usage,
            "cache_size": cache_size,
        }

        # Alert conditions
        if memory_usage > 0.9:
            status["warnings"] = ["High memory usage"]

        return status
    except Exception as e:
        return {"healthy": False, "error": str(e)}
```

## Logging

### Log Format

```
2024-01-15 10:30:45 [INFO] app.model_manager: Model loaded: yolov8n.pt (handler=YOLOHandler, load_time=0.52s)
2024-01-15 10:30:46 [WARNING] app.model_manager: Memory pressure, evicting model: yolov8x.pt
2024-01-15 10:30:47 [ERROR] app.handlers.yolo_handler: YOLO GPU memory exhausted: CUDA out of memory
```

### Log Levels

Set via environment variable:

```bash
export LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Structured Logging (Future)

```python
# Recommended format for production
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "logger": "app.model_manager",
  "message": "Model loaded",
  "model_id": "yolov8n.pt",
  "load_time": 0.52,
  "handler": "YOLOHandler"
}
```
