---
title: ADR-003 - TTL + LRU Hybrid Caching
---

# ADR-003: TTL + LRU Hybrid Caching

| Status | Date | Decision Makers |
|--------|------|-----------------|
| Accepted | 2024-01-20 | Architecture Team |

## Context

Model loading is expensive:
- YOLO models: 100ms - 2s
- HuggingFace models: 1s - 10s (network + deserialization)
- GPU memory: Limited, models consume 10MB - 500MB each

We needed a caching strategy that:
1. Avoids repeated loading costs
2. Prevents memory exhaustion
3. Handles varying model sizes
4. Supports concurrent access
5. Provides observability

## Decision

We implemented a **TTL + LRU Hybrid Cache**:
- TTLCache base class for time-based expiration
- LRU eviction when memory exceeds threshold
- Thread-safe access with locks
- Memory pressure monitoring

```python
class ModelCache(TTLCache):
    def __init__(self, maxsize, ttl, memory_threshold=0.85):
        super().__init__(maxsize=maxsize, ttl=ttl)
        self._access_times: dict[str, float] = {}
        self._lock = threading.Lock()
        self._memory_threshold = memory_threshold

    def __setitem__(self, key, value):
        with self._lock:
            if (len(self) >= self.maxsize or
                get_memory_usage() > self._memory_threshold):
                self._evict_lru_unsafe()
            super().__setitem__(key, value)
```

## Alternatives Considered

### Alternative 1: No Caching

Load model on every request:

```python
def infer(model_id, image):
    handler = get_handler(model_id)
    model = handler.load(model_id)  # Fresh load every time
    return model.infer(image)
```

**Pros**:
- Simple, no state management
- No memory concerns
- Fresh model state guaranteed

**Cons**:
- High latency (1-10s per request)
- Wastes CPU on repeated loading
- Poor user experience

### Alternative 2: Unbounded Cache

Cache all loaded models forever:

```python
_cache: dict[str, LoadedModel] = {}

def load_model(model_id):
    if model_id not in _cache:
        _cache[model_id] = handler.load(model_id)
    return _cache[model_id]
```

**Pros**:
- Maximum cache hit rate
- Simple implementation

**Cons**:
- Memory unbounded (OOM risk)
- No cleanup mechanism
- Stale models persist indefinitely

### Alternative 3: TTL-Only Cache

Use TTL without size/memory limits:

```python
cache = TTLCache(maxsize=float('inf'), ttl=3600)
```

**Pros**:
- Automatic cleanup after TTL
- No size management complexity

**Cons**:
- Memory can spike before TTL expires
- Popular models reloaded every TTL period
- No memory pressure awareness

### Alternative 4: LRU-Only Cache

Use LRU without TTL:

```python
cache = LRUCache(maxsize=10)
```

**Pros**:
- Bounded size
- Popular models stay cached

**Cons**:
- Popular models never refreshed
- Memory pressure not considered
- Stale models persist while popular

### Alternative 5: Weighted Cache

Weight entries by model size:

```python
class WeightedCache:
    def __init__(self, max_bytes):
        self.max_bytes = max_bytes
        self.current_bytes = 0
        self.entries = {}

    def set(self, key, value, weight):
        while self.current_bytes + weight > self.max_bytes:
            self._evict_lru()
        self.entries[key] = (value, weight)
        self.current_bytes += weight
```

**Pros**:
- Precise memory control
- Fair across different model sizes

**Cons**:
- Model sizes hard to estimate (varies by device)
- Complex implementation
- Weight calculation overhead

## Consequences

### Positive

1. **Responsiveness**: Cached models return instantly
2. **Memory Safety**: Eviction prevents OOM
3. **Freshness**: TTL ensures periodic refresh
4. **Thread Safety**: Concurrent access safe
5. **Configurable**: Environment variables tune behavior

### Negative

1. **Lock Overhead**: Contention under high concurrency
2. **Eviction Pauses**: GC/CUDA cleanup during eviction
3. **Configuration Complexity**: Three parameters to tune

### Mitigations

- **Lock Overhead**: Minimal due to Python GIL
- **Eviction Pauses**: Infrequent, acceptable latency
- **Configuration Complexity**: Sensible defaults (maxsize=10, ttl=3600, threshold=0.85)

## Implementation Notes

### Eviction Logic

```python
def _evict_lru_unsafe(self):
    # Find least recently accessed
    oldest_key = min(self._access_times, key=lambda k: self._access_times[k])

    # Remove from cache
    self.pop(oldest_key, None)
    self._access_times.pop(oldest_key, None)

    # Aggressive cleanup
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
```

### Memory Monitoring

```python
def get_memory_usage() -> float:
    try:
        import psutil
        return psutil.virtual_memory().percent / 100
    except ImportError:
        return 0.0
```

### Configuration

```python
# Environment variables
MODEL_CACHE_MAXSIZE=10      # Max cached models
MODEL_CACHE_TTL=3600        # TTL in seconds
MODEL_MEMORY_THRESHOLD=0.85 # Eviction threshold
```

## Performance Characteristics

| Scenario | Behavior |
|----------|----------|
| Cache hit | ~1ms (dict lookup) |
| Cache miss | 100ms - 10s (model load) |
| Eviction | ~100ms (GC + CUDA cleanup) |
| Memory threshold | Checked on every insert |

## References

- [cachetools.TTLCache](https://cachetools.readthedocs.io/en/stable/#cachetools.TTLCache)
- [Cache Algorithms - Wikipedia](https://en.wikipedia.org/wiki/Cache_replacement_policies)
