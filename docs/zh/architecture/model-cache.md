# 模型缓存

`ModelCache` 是一个 **LRU + TTL 混合缓存**，用于在内存中管理模型实例。它是运行时中最关键的性能组件，因为模型加载比推理慢多个数量级。

## 为什么混合缓存很重要

视觉模型加载成本很高：

| Model family | Load time (CPU) | Load time (CUDA) | Memory footprint |
|-------------|-----------------|------------------|------------------|
| YOLOv8 Nano | ~0.3s | ~0.1s | ~6 MB |
| YOLOv8 Large | ~2.1s | ~0.5s | ~90 MB |
| DETR ResNet-50 | ~4.8s | ~1.2s | ~160 MB |
| BLIP Caption Large | ~8.2s | ~2.5s | ~1.1 GB |

如果没有缓存，每个请求都要承担这一成本。有了缓存，第一个请求支付加载成本，后续请求可以复用已温热的实例。

## 架构

`ModelCache` 继承自 `TTLCache`（来自 `cachetools`），并增加了三项能力：

```
┌─────────────────────────────────────────────────────────────┐
│  ModelCache (extends TTLCache)                              │
│  ├─ TTL eviction: keys expire after configurable duration   │
│  ├─ LRU eviction: oldest-accessed key removed under pressure│
│  ├─ Memory-aware: evicts when system RAM exceeds threshold  │
│  └─ Thread-safe: all operations under reentrant lock        │
└─────────────────────────────────────────────────────────────┘
```

## TTL 淘汰

每个缓存的模型都有一个生存时间。在 TTL 秒内未被访问后，条目将自动过期。这可以防止陈旧模型无限期占用内存。

默认 TTL：**3600 秒（1 小时）**

## 内存压力下的 LRU 淘汰

插入新模型时，缓存会检查两个条件：

1. **容量**：如果 `len(cache) >= maxsize`，淘汰最旧的条目
2. **内存压力**：如果 `psutil.virtual_memory().percent > threshold`（默认 85%），淘汰最旧的条目

```python
def __setitem__(self, key: str, value: Any) -> None:
    with self._lock:
        if len(self) >= self.maxsize or get_memory_usage() > self._memory_threshold:
            self._evict_lru_unsafe()
        super().__setitem__(key, value)
```

### 淘汰的副作用

当模型被淘汰时：

1. `LoadedModel` 引用被释放
2. 触发 Python 垃圾回收（`gc.collect()`）
3. 如果 CUDA 可用，调用 `torch.cuda.empty_cache()` 释放 GPU 内存

这确保了淘汰不仅仅是一次字典删除，而是一个**资源回收事件**。

## 线程安全

所有缓存操作（`__getitem__`、`__setitem__`、`__delitem__`）都包裹在 `threading.Lock()` 中。这是必要的，因为：

- FastAPI 在线程池中运行请求处理器
- 模型加载是 I/O 密集型（从 HuggingFace 下载）或 CPU 密集型（初始化 PyTorch 张量）
- 对同一模型的并发请求不能触发重复加载

该锁确保即使在并发加载激增时，缓存状态也是一致的。

## 缓存内省

`/metrics` 端点和内部日志会暴露缓存状态：

```python
{
    "cache_size": 2,
    "cache_maxsize": 3,
    "cache_ttl": 3600,
    "cached_models": ["yolov8n.pt", "facebook/detr-resnet-50"],
    "memory_usage": 0.42
}
```

这些遥测数据对于运营调优至关重要：如果 `cache_size` 始终处于 `cache_maxsize`，运维人员应考虑增加容量或缩短 TTL。

## 调优指南

| Concern | Recommendation |
|---------|---------------|
| 低延迟，内存充足 | 增加 `cache_maxsize` 以覆盖所有轮换中的模型 |
| 内存受限 | 减少 `cache_maxsize` 和 `memory_threshold`；为热模型增加 TTL |
| 多模型轮换 | 将 `cache_maxsize` 设为 `n+1`，其中 `n` 为典型的并发模型数量 |
| GPU 内存受限 | 将 `memory_threshold` 设得更低（例如 0.75），以触发更早的淘汰 |

## 接下来阅读

- [系统概览](/zh/architecture/overview)，了解缓存在运行时拓扑中的位置
- [请求生命周期](/zh/architecture/request-flow)，了解缓存交互如何影响用户可见的行为
- [缓存策略](/zh/academy/caching-strategy)，了解混合方法背后的设计原理
