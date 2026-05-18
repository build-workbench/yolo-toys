# Request Lifecycle

This page follows one inference request through the runtime. The lifecycle matters because the quality of the public API depends on where the system translates, caches, validates, and formats.

<FigureFrame
  title="Figure 2. End-to-end lifecycle"
  caption="Requests enter through transport-specific surfaces but converge on a single coordination path before model-specific execution begins."
>
  <SvgRenderer src="/images/request-lifecycle.svg" alt="YOLO-Toys request lifecycle" title="Request Lifecycle" />
</FigureFrame>

## The path, step by step

1. **Ingress**: the request enters through HTTP or WebSocket.
2. **Validation**: parameters, files, and model identifiers are checked before execution starts.
3. **Coordination**: `ModelManager` selects or reuses the model instance and resolves the handler.
4. **Execution**: the selected handler runs model-family-specific inference.
5. **Normalization**: raw outputs are shaped into stable response contracts.
6. **Emission**: the runtime returns JSON or streamed frame-level payloads.

## Ingress and transport abstraction

The runtime supports two primary ingress surfaces:

- **HTTP REST API** (`/infer`, `/caption`, `/vqa`, `/models`, `/labels`, `/metrics`, `/health`)
- **WebSocket** (`/ws`) for real-time frame streaming

Both surfaces share the same underlying inference pipeline. The WebSocket handler wraps the HTTP path with frame-level streaming logic, so the core execution code does not bifurcate.

### WebSocket frame protocol

The WebSocket endpoint expects a JSON message per frame:

```json
{
  "model_id": "yolov8n.pt",
  "image": "base64-encoded-image-data",
  "conf": 0.25,
  "iou": 0.45,
  "max_det": 300
}
```

Responses are streamed as JSON objects with a `frame_id` and `results` array, enabling real-time visualization without polling.

## Validation and parameter shaping

Before any model is touched, the runtime validates the request through Pydantic schemas:

```python
class InferenceParams(BaseModel):
    conf: float = Field(default=0.25, ge=0.0, le=1.0)
    iou: float = Field(default=0.45, ge=0.0, le=1.0)
    max_det: int = Field(default=300, ge=1, le=1000)
    device: str | None = None
    imgsz: int | None = None
    half: bool = False
    text_queries: list[str] | None = None
    question: str | None = None
```

This parameter object is passed **through the entire stack**, from route handler to `ModelManager` to `BaseHandler._infer_impl()`, ensuring type safety at every boundary.

## Why normalization sits after execution

Upstream models disagree on output shape, label semantics, confidence behavior, and auxiliary artifacts. If route handlers tried to normalize those differences directly, the transport layer would become the place where model semantics accumulate. YOLO-Toys instead keeps the route surface thin and lets handlers plus formatter helpers perform the translation.

### Normalization contract

Every handler returns a dictionary with a guaranteed schema:

```python
{
    "model_id": str,
    "inference_time_ms": float,
    "results": list[dict],
    "metadata": dict  # handler-specific, but always present
}
```

This means a client consuming the `/infer` endpoint receives the same envelope regardless of whether the backend is YOLOv8, DETR, or OWL-ViT.

## Cache and concurrency interactions

The lifecycle is not just functional, it is operational. A request path can trigger:

- a **cache hit** and immediate reuse of a warm model
- a **lazy model load** on first use, with the full cold-start latency borne by the first requester
- **waiting behind concurrency limits** when the runtime is already saturated

Those interactions are part of the user-visible behavior because they shape latency, warm-up cost, and resource pressure.

### Cold-start vs warm-start latency

| Scenario | Behavior | Typical latency impact |
|----------|----------|----------------------|
| Cache hit | Model already loaded, infer immediately | Baseline (device-dependent) |
| Lazy load | Download + init on first request | +2-10s for HF models, +0.5-2s for YOLO .pt |
| Memory pressure eviction | LRU evict + reload | Same as lazy load |

## Failure surfaces

Common failures cluster at four points:

- **invalid or oversized inputs**: caught at validation layer (Pydantic + OpenCV checks)
- **unknown model identifiers**: caught at registry resolution (`ModelCategory.infer_from_id()` raises `ValueError`)
- **runtime model-loading failures**: caught at handler `_do_load()`; includes network errors for HuggingFace downloads
- **downstream inference errors inside handlers**: caught at `BaseHandler._infer_impl()`; includes CUDA OOM and model-specific exceptions

The value of the current architecture is that each failure type has a natural boundary where it can be surfaced cleanly.

## What to read next

- [System Overview](/en/architecture/overview) for the layered runtime map
- [Handler Topology](/en/architecture/handlers) for how execution boundaries stay clean
- [Middleware Stack](/en/architecture/middleware-stack) for how observability and guardrails fit in
- [Model Cache](/en/architecture/model-cache) for the caching strategy in depth
