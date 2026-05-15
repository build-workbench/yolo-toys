---
title: 性能调优
---

# 性能调优

本指南介绍如何优化 YOLO-Toys 的性能。

## 推理优化

### FP16 半精度推理

启用 FP16 可减少约 50% 的显存占用和推理时间：

```bash
# 环境变量
export ENABLE_FP16=true

# 或在配置中
model_manager = ModelManager(config=ModelManagerConfig(
    enable_fp16=True
))
```

### 批处理

对于多图推理，使用批处理可显著提高吞吐量：

```python
# 单图推理（低效）
for image in images:
    result = model.infer(image, params)

# 批处理推理（高效）
results = model.infer_batch(images, params)
```

## 缓存优化

### TTL 配置

根据使用模式调整 TTL：

```python
# 高频使用场景：长 TTL
ModelManagerConfig(cache_ttl=3600)  # 1 小时

# 多模型切换场景：短 TTL
ModelManagerConfig(cache_ttl=300)   # 5 分钟
```

### LRU 驱逐

内存压力阈值配置：

```python
# 默认 80% GPU 内存时触发驱逐
ModelManagerConfig(memory_threshold=0.8)

# 更保守的设置
ModelManagerConfig(memory_threshold=0.6)
```

## GPU 优化

### 内存碎片整理

定期清理 CUDA 缓存：

```python
import torch
torch.cuda.empty_cache()
```

### 多 GPU 负载均衡

```python
# 指定 GPU 设备
handler = YOLOHandler(device="cuda:0")
handler2 = YOLOHandler(device="cuda:1")
```

## 网络优化

### 图片压缩

传输前压缩图片可减少网络延迟：

```python
from PIL import Image
import io

def compress_image(image, quality=85):
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    return buffer.getvalue()
```

### WebSocket 长连接

对于高频推理，使用 WebSocket 替代 REST：

```python
import websockets

async def infer_stream():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        for image in images:
            await ws.send(image)
            result = await ws.recv()
```

## 性能基准

| 配置 | 延迟 (P50) | 延迟 (P99) | 吞吐量 |
|------|-----------|-----------|--------|
| FP32, 单图 | 45ms | 80ms | 22 req/s |
| FP16, 单图 | 28ms | 50ms | 35 req/s |
| FP16, 批处理 4 | 15ms/图 | 25ms/图 | 80 req/s |

## 监控指标

关键监控指标：

- `inference_latency_ms`：推理延迟
- `model_cache_hit_rate`：缓存命中率
- `gpu_memory_used_percent`：GPU 内存使用率
- `requests_per_second`：请求吞吐量
