---
title: 监控告警
---

# 监控告警

本指南介绍 YOLO-Toys 的监控和告警配置。

## 内置指标

### Prometheus 指标

YOLO-Toys 在 `/metrics` 端点暴露 Prometheus 指标：

| 指标名 | 类型 | 说明 |
|--------|------|------|
| `yolo_toys_inference_requests_total` | Counter | 推理请求总数 |
| `yolo_toys_inference_duration_seconds` | Histogram | 推理延迟分布 |
| `yolo_toys_model_cache_size` | Gauge | 缓存中的模型数量 |
| `yolo_toys_gpu_memory_used_bytes` | Gauge | GPU 内存使用量 |
| `yolo_toys_gpu_memory_total_bytes` | Gauge | GPU 内存总量 |

### 健康检查

```bash
# 基础健康检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "models_cached": 3,
  "gpu_memory_used_percent": 45.2
}
```

## Prometheus 配置

### 抓取配置

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'yolo-toys'
    static_configs:
      - targets: ['yolo-toys:8000']
    metrics_path: /metrics
    scrape_interval: 15s
```

## Grafana 仪表盘

导入预配置仪表盘：

```bash
# 使用仪表盘 JSON
grafana-cli dashboards import dashboard.json
```

关键面板：
- 推理延迟 P50/P95/P99
- 请求吞吐量
- GPU 内存使用率
- 缓存命中率
- 错误率

## 告警规则

### Prometheus AlertManager 规则

```yaml
# alerts.yml
groups:
- name: yolo-toys
  rules:
  - alert: HighInferenceLatency
    expr: histogram_quantile(0.99, rate(yolo_toys_inference_duration_seconds_bucket[5m])) > 0.5
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "高推理延迟"
      description: "P99 延迟超过 500ms"

  - alert: HighGPUMemoryUsage
    expr: yolo_toys_gpu_memory_used_bytes / yolo_toys_gpu_memory_total_bytes > 0.9
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "GPU 内存使用过高"
      description: "GPU 内存使用率超过 90%"

  - alert: LowCacheHitRate
    expr: rate(yolo_toys_cache_hits_total[5m]) / rate(yolo_toys_cache_requests_total[5m]) < 0.5
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "缓存命中率低"
      description: "缓存命中率低于 50%"
```

## 日志配置

### 结构化日志

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "extra": getattr(record, "extra", {})
        })
```

### 日志级别

| 级别 | 用途 |
|------|------|
| DEBUG | 开发调试 |
| INFO | 正常操作 |
| WARNING | 潜在问题 |
| ERROR | 错误情况 |
| CRITICAL | 严重故障 |
