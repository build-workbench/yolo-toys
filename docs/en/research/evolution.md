# Evolution of the Architecture

This chapter traces how YOLO-Toys arrived at its current design. It is not a changelog; it is a narrative of architectural decisions, dead ends, and the reasoning that made the current boundaries necessary.

## From flat endpoints to a handler boundary

The earliest version of the runtime exposed one FastAPI endpoint per model family:

```python
@app.post("/yolo/infer")
async def yolo_infer(...): ...

@app.post("/detr/infer")
async def detr_infer(...): ...
```

This worked for two families. It did not work for five. Each new family duplicated:

- parameter validation
- image preprocessing
- model loading logic
- result formatting
- error handling

The duplication was not just code; it was **conceptual**. Every endpoint reimplemented the same "load a model, run inference, return JSON" contract.

### The extraction

The first architectural move was to extract a `BaseHandler` with two abstract methods:

```python
class BaseHandler(ABC):
    def _do_load(self, model_id: str) -> tuple[Any, Any | None]: ...
    def _infer_impl(self, model, processor, image, params) -> dict: ...
```

This is the **Template Method pattern** applied to model inference. The `ModelManager` calls `handler.load()` and `loaded.infer()` without knowing which family is underneath. Each handler subclass owns its family's quirks: YOLO uses `ultralytics.YOLO`, DETR uses `transformers.DetrForObjectDetection`, BLIP uses `BlipProcessor` and `BlipForConditionalGeneration`.

### The cost of the boundary

The handler boundary is not free. It adds:

- one indirection per inference call
- the need for a registry to map model IDs to handler classes
- the discipline to keep family-specific code inside the handler

The trade-off is worth it because the alternative—family logic scattered across route handlers—scales poorly in both code volume and cognitive load.

## From hardcoded dispatch to registry inference

The second evolution was dispatch. Initially, the manager used a hardcoded `if/elif` chain:

```python
if "yolo" in model_id:
    handler = YOLOHandler(device)
elif "detr" in model_id:
    handler = DETRHandler(device)
```

This was brittle. Adding a new family meant touching `ModelManager`. The fix was to move dispatch into a registry with **category inference**:

```python
class ModelCategory(Enum):
    YOLO_DETECT = auto()
    HF_DETR = auto()
    HF_OWLVIT = auto()
    # ...

    @classmethod
    def infer_from_id(cls, model_id: str) -> "ModelCategory": ...
```

The `HandlerRegistry` maps categories to handler classes. The manager asks the registry for a handler, and the registry infers the category from the model ID.

### Self-healing inference

The inference chain is designed to be **self-healing** for common conventions:

1. Exact registry lookup for known models
2. `.pt` extension → YOLO family
3. Keyword matching (`detr`, `owlvit`, `blip`, etc.)
4. HuggingFace path (`/`) → DETR fallback

This means that adding a new YOLOv8 weights file does not require a registry entry. But adding a completely new model family (e.g., RT-DETR) does require extending `ModelCategory` and `_CATEGORY_HANDLER_MAP`.

## From naive caching to operational awareness

The first cache was a plain dictionary:

```python
self._cache: dict[str, Any] = {}
```

It held models indefinitely. It was not thread-safe. It had no eviction policy. On a GPU with limited VRAM, this was a recipe for OOM crashes.

The current `ModelCache` is a **third-generation** design:

| Generation | Eviction | Thread safety | Memory awareness |
|-----------|-----------|---------------|----------------|
| v1: dict | None | No | No |
| v2: TTLCache | TTL only | No | No |
| v3: ModelCache | LRU + TTL | Yes | Yes |

The LRU + TTL hybrid is the minimal viable cache for a production vision serving runtime. It is not a distributed cache, it is not a persistent cache, and it does not do model quantization. But it solves the right problem: **keep hot models warm without exhausting host memory**.

## The OpenSpec layer

The most recent architectural addition is the OpenSpec system: a set of specifications and change artifacts that document the runtime's behavior before code is written.

This is unusual for a project of this size. Most repositories this small rely on README + code. YOLO-Toys adds OpenSpec because the target audience—interviewers, reviewers, contributors—needs **traceable design rationale**, not just working code.

The OpenSpec workflow:

1. **Explore** (`/opsx:explore`) — investigate a problem or idea
2. **Propose** (`/opsx:propose`) — write a specification with design, tasks, and acceptance criteria
3. **Apply** (`/opsx:apply`) — implement from the specification
4. **Review** (`/review`) — verify at phase boundaries
5. **Archive** (`/opsx:archive`) — clean up completed changes

This workflow keeps the repository in a **documented state** rather than an ad-hoc state.

## Future directions

The architecture is not frozen. These are the active areas of investigation:

| Direction | Status | Open questions |
|-----------|--------|---------------|
| Batch inference | Proposed | How to batch heterogeneous model families without losing per-request semantics |
| Model quantization | Research | INT8/FP16 quantization trade-offs per family; memory vs accuracy |
| Streaming protocol v2 | Design | Binary frame encoding (MessagePack or protobuf) for lower WebSocket overhead |
| Multi-GPU sharding | Future | How to distribute model cache across multiple CUDA devices |
| gRPC surface | Future | Whether gRPC adds enough latency benefit to justify the complexity |

## What to read next

- [Bibliography](/en/citations) for the papers and projects that influenced these decisions
- [Handler Pattern](/en/academy/handler-pattern) for the design pattern deep dive
- [Caching Strategy](/en/academy/caching-strategy) for the cache design rationale
