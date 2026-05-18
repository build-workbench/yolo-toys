# Architecture Overview

YOLO-Toys is easiest to understand as a **normalized serving runtime**. The goal is not to hide the fact that different vision models behave differently. The goal is to make those differences live behind explicit execution boundaries instead of leaking into every route, payload, and deployment concern.

<FigureFrame
  title="Figure 1. Runtime topology"
  caption="The service is deliberately layered so route handling, model resolution, execution, caching, and result shaping do not collapse into the same abstraction."
>
  <SvgRenderer src="/images/hero-architecture.svg" alt="YOLO-Toys runtime topology" title="Runtime Topology" />
</FigureFrame>

## Layer model

| Layer | Responsibility | Why it exists |
| --- | --- | --- |
| API surface | HTTP and WebSocket ingress | Keeps transport concerns separate from model logic |
| Runtime coordination | `ModelManager`, concurrency controls, cache policy | Centralizes lifecycle and resource decisions |
| Dispatch and metadata | `HandlerRegistry`, model registry entries | Makes model lookup deterministic and inspectable |
| Execution adapters | YOLO, DETR, OWL-ViT, Grounding DINO, BLIP handlers | Contains model-family-specific behavior |
| Result normalization | shared schemas and formatter helpers | Preserves a coherent public contract |

## The central architectural bet

The project makes one strong bet: **heterogeneous models can share a service boundary if their execution differences are pushed into handler adapters and their public outputs are normalized aggressively enough**.

That bet creates three wins:

1. API consumers do not need a different integration style per model family.
2. New model families can be added with limited surface churn.
3. Architectural trade-offs stay visible because the adapters remain explicit.

It also creates one cost:

- the runtime must own more translation work between upstream model semantics and downstream API semantics

## Why the manager layer is central

`ModelManager` is not a convenience wrapper. It is the runtime's control plane. It decides when models are loaded, when cached instances should be reused, and how inference requests move toward the right handler without route-level duplication.

### Security boundary at load time

The manager enforces path-traversal protection before any model is loaded:

```python
# From app/model_manager.py
decoded_id = urllib.parse.unquote(model_id)
forbidden_patterns = ["../", "..\\", "/", "\\", "\x00"]
for pattern in forbidden_patterns:
    if pattern in model_id or pattern in decoded_id:
        raise ValueError("Invalid model ID: contains forbidden character sequence")
```

This is a deliberate security posture: model IDs are treated as untrusted input, decoded, and pattern-matched against a deny-list before reaching the registry or filesystem.

### LRU + TTL hybrid cache

The `ModelCache` extends `TTLCache` from `cachetools` with two additional capabilities:

- **LRU eviction under memory pressure**: when system memory exceeds a configurable threshold (default 85%), the least-recently-used model is evicted
- **Thread-safe access**: all cache operations are wrapped in a reentrant lock
- **CUDA cache clearing**: when a model is evicted, `torch.cuda.empty_cache()` is called to release GPU memory

```python
class ModelCache(TTLCache[str, LoadedModel]):
    def __setitem__(self, key: str, value: Any) -> None:
        with self._lock:
            if len(self) >= self.maxsize or get_memory_usage() > self._memory_threshold:
                self._evict_lru_unsafe()
            super().__setitem__(key, value)
```

This design means the cache is **operationally aware**: it does not just expire keys by time; it also reacts to host resource pressure.

## Why the registry matters

The registry is the project's **semantic index**. It does more than map IDs to handlers. It records model category, task type, metadata, and parameter expectations. That makes the service introspectable through `/models`, keeps dispatch deterministic, and gives the docs a single factual backbone.

### Category inference logic

`ModelCategory.infer_from_id()` implements a cascading resolution strategy:

1. **Exact registry match**: if the model ID is in `MODEL_REGISTRY`, use the registered category
2. **File extension heuristic**: `.pt` files are classified as YOLO (with `seg`/`pose` sub-variants)
3. **HuggingFace path inference**: `detr`, `owlvit`, `grounding`, `dino`, `blip` keywords map to respective categories
4. **Fallback**: any ID containing `/` is treated as a HuggingFace DETR model

This inference chain means the registry is **self-healing** for common naming conventions while remaining strict for unknown inputs.

## Middleware stack design

The runtime ships with a layered middleware stack that reflects production concerns:

```
SecurityHeaders → Metrics → Timeout → RateLimit → GZip → CORS → Application
```

| Middleware | Concern | Key behavior |
|------------|---------|------------|
| `SecurityHeadersMiddleware` | Response security | Adds X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy, Permissions-Policy |
| `MetricsMiddleware` | Observability | Records request duration histograms via Prometheus; samples memory usage every 10s |
| `TimeoutMiddleware` | Resilience | Warns when requests exceed a configurable threshold (default 60s) |
| `RateLimitMiddleware` | Abuse prevention | Per-IP token bucket in memory; auto-cleans expired entries to prevent memory leaks |
| `GZipMiddleware` | Bandwidth | Compresses responses above a size threshold |
| `CORSMiddleware` | Cross-origin | Restricted to configured origin list; disables credentials when `*` is used |

Read the full middleware analysis in [Middleware Stack](/en/architecture/middleware-stack).

## What to read next

- [Request Lifecycle](/en/architecture/request-flow) for the end-to-end inference path
- [Handler Pattern](/en/academy/handler-pattern) for the adapter boundary
- [Registry Pattern](/en/academy/registry-pattern) for model metadata and dispatch reasoning
- [Middleware Stack](/en/architecture/middleware-stack) for the operational layers
- [Config Injection](/en/architecture/config-injection) for how settings flow through the system
- [Model Cache](/en/architecture/model-cache) for the caching strategy in depth
