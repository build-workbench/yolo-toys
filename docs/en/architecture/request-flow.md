---
title: Request Flow - End-to-End Processing
---

# Request Flow: End-to-End Processing

This document traces a complete inference request from HTTP receipt to response, showing how each component participates.

## High-Level Flow

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Middleware
    participant Router
    participant ModelManager
    participant ModelCache
    participant HandlerRegistry
    participant Handler
    participant LoadedModel
    participant Model

    Client->>FastAPI: POST /infer (image, params)
    FastAPI->>Middleware: process request

    Note over Middleware: Security Headers, Rate Limit, Metrics

    Middleware->>Router: infer()
    Router->>Router: read_upload_image()
    Router->>Router: parse params

    Router->>ModelManager: infer(model_id, image, params)

    ModelManager->>ModelCache: check cache
    alt Cache Hit
        ModelCache-->>ModelManager: LoadedModel
    else Cache Miss
        ModelManager->>HandlerRegistry: get_handler(model_id)
        HandlerRegistry->>HandlerRegistry: resolve category
        HandlerRegistry-->>ModelManager: Handler instance

        ModelManager->>Handler: load(model_id)
        Handler->>Model: load model
        Model-->>Handler: model object
        Handler-->>ModelManager: LoadedModel

        ModelManager->>ModelCache: store LoadedModel
    end

    ModelManager->>LoadedModel: infer(image, params)
    LoadedModel->>Handler: _infer_impl(model, processor, image, params)
    Handler->>Handler: preprocess image
    Handler->>Model: run inference
    Model-->>Handler: raw results
    Handler->>Handler: postprocess results
    Handler-->>LoadedModel: result dict
    LoadedModel-->>ModelManager: result dict

    ModelManager-->>Router: result dict
    Router->>Router: add model_id to result
    Router-->>Client: JSON response
```

## Detailed Component Flow

### 1. HTTP Request Reception

```python
# app/api/inference.py
@router.post("/infer")
async def infer(
    file: UploadFile,
    model: str | None = None,
    conf: float | None = None,
    ...
):
    # Semaphore for concurrency control
    async with semaphore:
        result = await asyncio.to_thread(
            model_manager.infer,
            model_id=model_id,
            image=img,
            ...
        )
```

### 2. Middleware Chain

```python
# app/main.py
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(TimeoutMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware)
```

**Order matters**: Added first, executed last (wraps subsequent middleware).

### 3. Image Processing

```python
# app/api/utils.py
async def read_upload_image(file: UploadFile) -> tuple[np.ndarray, int]:
    content = await file.read()
    nparr = np.frombuffer(content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # BGR format
    return image, len(content)
```

### 4. Model Resolution

```python
# app/model_manager.py
def load_model(self, model_id: str) -> LoadedModel:
    if model_id in self._cache:
        return self._cache[model_id]

    handler = self._registry.get_handler(model_id)
    loaded = handler.load(model_id)
    self._cache[model_id] = loaded
    return loaded
```

### 5. Handler Resolution

```python
# app/handlers/registry.py
def get_handler(self, model_id: str) -> BaseHandler:
    category = ModelCategory.infer_from_id(model_id, MODEL_REGISTRY)
    handler_cls = _CATEGORY_HANDLER_MAP[category]
    return handler_cls(self._config_or_device)
```

### 6. Model Loading

```python
# app/handlers/base.py
def load(self, model_id: str) -> LoadedModel:
    model, processor = self._do_load(model_id)
    return LoadedModel(model, processor, self, model_id)
```

### 7. Inference Execution

```python
# app/handlers/base.py (LoadedModel)
def infer(self, image: np.ndarray, params: InferenceParams) -> dict:
    return self._handler._infer_impl(
        self._model, self._processor, image, params
    )
```

### 8. Result Formatting

```python
# app/handlers/utils.py
def make_result(image, *, detections, inference_time, task, **extra):
    h, w = image.shape[:2]
    return {
        "width": w,
        "height": h,
        "inference_time": inference_time,
        "task": task,
        "detections": detections,
        **extra
    }
```

## WebSocket Flow

```mermaid
sequenceDiagram
    participant Client
    participant WebSocket
    participant Parser
    participant ModelManager
    participant Handler

    Client->>WebSocket: connect (ws://host/ws?model=yolov8n.pt)
    WebSocket->>Parser: parse query params
    WebSocket-->>Client: {"type": "ready", "model": "yolov8n.pt"}

    loop For each frame
        Client->>WebSocket: binary frame (image)
        WebSocket->>Parser: decode image

        alt Valid image
            WebSocket->>ModelManager: infer(model_id, image, params)
            ModelManager-->>WebSocket: result dict
            WebSocket-->>Client: {"type": "result", "data": {...}}
        else Invalid image
            WebSocket-->>Client: {"type": "error", "detail": "..."}
        end
    end

    Client->>WebSocket: close
    WebSocket-->>Client: connection closed
```

## Error Handling Flow

```mermaid
flowchart TD
    A[Request] --> B{Valid Image?}
    B -->|No| C[400 Bad Request]
    B -->|Yes| D{Valid Model?}
    D -->|No| E[404 Not Found]
    D -->|Yes| F{Memory Available?}
    F -->|No| G[503 Service Unavailable]
    F -->|Yes| H{Inference Success?}
    H -->|No| I[500 Internal Error]
    H -->|Yes| J[200 OK + Result]

    C --> K[Log Error]
    E --> K
    G --> K
    I --> K
    J --> L[Update Metrics]
```

## Timing Breakdown

| Phase | Typical Duration | Notes |
|-------|------------------|-------|
| HTTP parsing | < 1ms | FastAPI overhead |
| Image decode | 1-10ms | Depends on size |
| Cache lookup | < 1ms | Dict access |
| Model load | 100ms - 10s | First load only |
| Preprocessing | 1-50ms | Model-specific |
| Inference | 10ms - 1s | GPU/CPU dependent |
| Postprocessing | 1-10ms | Format conversion |
| JSON encode | < 1ms | Response size dependent |

## Metrics Collection

Each request updates Prometheus metrics:

```python
INFERENCE_REQUESTS.labels(model, task, status).inc()
INFERENCE_LATENCY.labels(model, task).observe(duration)
INFERENCE_INPUT_SIZE.observe(file_size)
```

Access metrics at `/metrics` endpoint for Prometheus scraping.
