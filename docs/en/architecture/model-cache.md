# Model Cache

The `ModelCache` is a **LRU + TTL hybrid cache** that manages model instances in memory. It is the single most performance-critical component of the runtime because model loading is orders of magnitude slower than inference.

## Why hybrid caching matters

Vision models are expensive to load:

| Model family | Load time (CPU) | Load time (CUDA) | Memory footprint |
|-------------|-----------------|------------------|------------------|
| YOLOv8 Nano | ~0.3s | ~0.1s | ~6 MB |
| YOLOv8 Large | ~2.1s | ~0.5s | ~90 MB |
| DETR ResNet-50 | ~4.8s | ~1.2s | ~160 MB |
| BLIP Caption Large | ~8.2s | ~2.5s | ~1.1 GB |

Without caching, every request would pay this cost. With caching, the first request pays the load cost and subsequent requests reuse the warm instance.

## Architecture

`ModelCache` inherits from `TTLCache` (from `cachetools`) and adds three capabilities:

```
┌─────────────────────────────────────────────────────────────┐
│  ModelCache (extends TTLCache)                              │
│  ├─ TTL eviction: keys expire after configurable duration   │
│  ├─ LRU eviction: oldest-accessed key removed under pressure│
│  ├─ Memory-aware: evicts when system RAM exceeds threshold  │
│  └─ Thread-safe: all operations under reentrant lock        │
└─────────────────────────────────────────────────────────────┘
```

## TTL eviction

Each cached model has a time-to-live. After TTL seconds without access, the entry is automatically expired. This prevents stale models from consuming memory indefinitely.

Default TTL: **3600 seconds (1 hour)**

## LRU eviction under memory pressure

When inserting a new model, the cache checks two conditions:

1. **Capacity**: if `len(cache) >= maxsize`, evict the oldest item
2. **Memory pressure**: if `psutil.virtual_memory().percent > threshold` (default 85%), evict the oldest item

```python
def __setitem__(self, key: str, value: Any) -> None:
    with self._lock:
        if len(self) >= self.maxsize or get_memory_usage() > self._memory_threshold:
            self._evict_lru_unsafe()
        super().__setitem__(key, value)
```

### Eviction side effects

When a model is evicted:

1. The `LoadedModel` reference is dropped
2. Python garbage collection is triggered (`gc.collect()`)
3. If CUDA is available, `torch.cuda.empty_cache()` is called to release GPU memory

This ensures that eviction is not just a dictionary deletion but a **resource reclamation event**.

## Thread safety

All cache operations (`__getitem__`, `__setitem__`, `__delitem__`) are wrapped in a `threading.Lock()`. This is necessary because:

- FastAPI runs request handlers in a thread pool
- Model loading is I/O-bound (downloading from HuggingFace) or CPU-bound (initializing PyTorch tensors)
- Concurrent requests for the same model must not trigger duplicate loads

The lock ensures that the cache state is consistent even under concurrent load bursts.

## Cache introspection

The `/metrics` endpoint and internal logging expose cache state:

```python
{
    "cache_size": 2,
    "cache_maxsize": 3,
    "cache_ttl": 3600,
    "cached_models": ["yolov8n.pt", "facebook/detr-resnet-50"],
    "memory_usage": 0.42
}
```

This telemetry is critical for operational tuning: if `cache_size` is always at `cache_maxsize`, the operator should consider increasing capacity or shortening TTL.

## Tuning guidelines

| Concern | Recommendation |
|---------|---------------|
| Low latency, memory abundant | Increase `cache_maxsize` to cover all models in rotation |
| Memory constrained | Reduce `cache_maxsize` and `memory_threshold`; increase TTL for hot models |
| Multi-model rotation | Set `cache_maxsize` to `n+1` where `n` is the typical concurrent model count |
| GPU memory constrained | Set `memory_threshold` lower (e.g., 0.75) to trigger earlier eviction |

## What to read next

- [System Overview](/en/architecture/overview) for where caching fits in the runtime topology
- [Request Lifecycle](/en/architecture/request-flow) for how cache interactions shape user-visible behavior
- [Caching Strategy](/en/academy/caching-strategy) for the design rationale behind the hybrid approach
