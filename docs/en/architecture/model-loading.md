---
title: Model Loading Flow
---

# Model Loading Flow

The model loading subsystem is the heart of YOLO-Toys' operational behavior. It combines lazy loading, TTL-based freshness, and LRU eviction under memory pressure to provide predictable resource usage while maximizing warm-model reuse.

<SvgRenderer src="/images/model-loading.svg" alt="Model loading flow diagram" />

## The Core Problem

Serving multiple model families creates a fundamental tension:

1. **Loading models is expensive** — YOLOv8x takes 2-4 seconds to load on a modern GPU
2. **Memory is finite** — A single YOLOv8x can consume 200MB+ of GPU memory
3. **Workloads are bursty** — Users don't request models uniformly

The solution must balance:
- **Latency**: Minimize cold-start penalties
- **Memory**: Stay within hardware limits
- **Freshness**: Respect model update cycles

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      ModelManager                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐ │
│  │  Security Check │→│  Cache Lookup   │→│ Handler Select│ │
│  └─────────────────┘  └─────────────────┘  └───────────────┘ │
│                              ↓                                 │
│                    ┌─────────────────┐                        │
│                    │  ModelCache     │                        │
│                    │  (TTL + LRU)    │                        │
│                    └─────────────────┘                        │
└──────────────────────────────────────────────────────────────┘
```

## Cache Strategy: TTL + LRU Hybrid

### Why Both?

| Strategy | What it Guarantees | What it Misses |
|----------|-------------------|----------------|
| **TTL only** | Freshness (models expire) | No memory pressure handling |
| **LRU only** | Memory bounds | Stale models persist forever |
| **TTL + LRU** | Both freshness and bounds | Complexity |

The hybrid approach gives us the best of both worlds.

### TTL (Time-To-Live)

```python
# Default: 3600 seconds (1 hour)
MODEL_CACHE_TTL = int(os.getenv("MODEL_CACHE_TTL", "3600"))
```

When a model's TTL expires:
- The model is marked as stale
- Next access triggers a reload
- The old model is evicted from cache

### LRU (Least Recently Used)

```python
# Default: 10 models max
MODEL_CACHE_MAXSIZE = int(os.getenv("MODEL_CACHE_MAXSIZE", "10"))
```

When cache is full and a new model is requested:
- Find the least recently accessed model
- Evict it (freeing GPU memory)
- Load the new model

### Memory-Aware Eviction

```python
# Default: 85% of system memory
MODEL_MEMORY_THRESHOLD = float(os.getenv("MODEL_MEMORY_THRESHOLD", "0.85"))
```

Even if the cache isn't full, if system memory usage exceeds the threshold:
- Trigger proactive LRU eviction
- Clear CUDA cache to reclaim GPU memory

```python
def _evict_lru_unsafe(self) -> None:
    """Evict least recently used model and clear CUDA cache."""
    lru_key = min(self._access_times, key=self._access_times.get)
    del self[lru_key]
    torch.cuda.empty_cache()  # Critical for GPU memory
```

## Security Boundary

Before any model load, the request passes through security validation:

```python
# Path traversal protection
forbidden_patterns = ["../", "..\\", "/", "\\", "\x00"]
for pattern in forbidden_patterns:
    if pattern in model_id or pattern in decoded_id:
        raise ValueError("Invalid model ID: forbidden pattern")
```

This prevents:
- Directory traversal attacks (`../../../etc/passwd`)
- URL-encoded bypasses (`%2e%2e%2f`)
- Null byte injection (`model.pt%00.exe`)

## Handler Selection

The registry maps model categories to handlers:

```python
class ModelCategory(Enum):
    YOLO_DETECT = auto()
    YOLO_SEGMENT = auto()
    YOLO_POSE = auto()
    HF_DETR = auto()
    HF_OWLVIT = auto()
    HF_GROUNDING_DINO = auto()
    MULTIMODAL_CAPTION = auto()
    MULTIMODAL_VQA = auto()
```

Category resolution follows a priority chain:

1. **Exact registry match** — `MODEL_REGISTRY.get(model_id)`
2. **File extension heuristic** — `.pt` → YOLO
3. **HuggingFace path inference** — `detr`, `owlvit`, `grounding`, `blip` keywords
4. **Fallback** — Any path with `/` → DETR (HuggingFace)

## Thread Safety

Model loading is protected by a reentrant lock:

```python
self._lock = threading.RLock()

def get_model(self, model_id: str) -> LoadedModel:
    with self._lock:
        # Thread-safe cache access
        if model_id in self._cache:
            return self._cache[model_id]
        # Load and cache
        model = self._load_model(model_id)
        self._cache[model_id] = model
        return model
```

This ensures:
- No race conditions when multiple requests hit a cold cache
- Atomic check-then-load operations
- Safe concurrent access from async handlers

## Configuration Reference

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `MODEL_CACHE_MAXSIZE` | `10` | Maximum cached models |
| `MODEL_CACHE_TTL` | `3600` | Cache TTL in seconds |
| `MODEL_MEMORY_THRESHOLD` | `0.85` | Memory threshold (0-1) |
| `MAX_CONCURRENCY` | `4` | Max concurrent inferences |
| `SKIP_WARMUP` | `false` | Skip model warmup on startup |

## What to Read Next

<CrossReference href="/en/architecture/handlers" section="Architecture" label="Handler Topology" />
<CrossReference href="/en/academy/caching-strategy" section="Academy" label="Caching Strategy Deep Dive" />
