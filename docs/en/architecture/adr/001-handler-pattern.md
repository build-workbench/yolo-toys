---
title: ADR-001 - Handler Pattern over Factory Pattern
---

# ADR-001: Handler Pattern over Factory Pattern

| Status | Date | Decision Makers |
|--------|------|-----------------|
| Accepted | 2024-01-15 | Architecture Team |

## Context

YOLO-Toys needed to support multiple model families with vastly different inference pipelines:

- **YOLO models**: Load via `ultralytics.YOLO()`, return `Results` objects
- **HuggingFace models**: Load via `AutoModel.from_pretrained()`, require pre/post processors
- **Multimodal models**: Additional inputs like text queries or questions

Each model family has unique:
- Loading mechanisms
- Preprocessing requirements
- Output formats
- Configuration parameters

We needed an architecture that could:
1. Provide a unified interface to callers
2. Encapsulate family-specific logic
3. Support easy extension for new models
4. Maintain testability

## Decision

We adopted the **Strategy Pattern (Handler Pattern)** where:
- `BaseHandler` defines the abstract interface
- Each model family has a concrete handler implementation
- `LoadedModel` wraps the loaded model with a simple `infer()` interface
- `HandlerRegistry` resolves model IDs to appropriate handlers

```python
# The Strategy Pattern approach
class BaseHandler(ABC):
    @abstractmethod
    def _do_load(self, model_id: str) -> tuple[Any, Any | None]: ...

    @abstractmethod
    def _infer_impl(self, model, processor, image, params) -> dict: ...

# Concrete strategies
class YOLOHandler(BaseHandler): ...
class DETRHandler(BaseHandler): ...
class BLIPCaptionHandler(BaseHandler): ...
```

## Alternatives Considered

### Alternative 1: Factory Pattern

Create a factory that produces inference functions:

```python
class InferenceFactory:
    @staticmethod
    def create(model_id: str) -> Callable:
        if model_id.endswith(".pt"):
            return YOLOInference(model_id)
        elif "detr" in model_id:
            return DETRInference(model_id)
        ...

# Usage
infer = InferenceFactory.create("yolov8n.pt")
result = infer(image)
```

**Pros**:
- Simple to understand
- No class hierarchy needed

**Cons**:
- Doesn't encapsulate state (loaded model, processor)
- Harder to share common logic (device management, error handling)
- Returns functions, not objects with rich interfaces

### Alternative 2: Switch/Case Dispatch

Central dispatch with if/elif chains:

```python
def infer(model_id: str, image, **params):
    if model_id.endswith(".pt"):
        model = load_yolo(model_id)
        return yolo_infer(model, image, params)
    elif "detr" in model_id:
        model, processor = load_detr(model_id)
        return detr_infer(model, processor, image, params)
    elif "owlvit" in model_id:
        ...
```

**Pros**:
- Simple, no abstraction overhead
- Easy to see all paths in one place

**Cons**:
- Single file grows indefinitely
- No encapsulation per model family
- Hard to unit test individual families
- Violates Open/Closed Principle

### Alternative 3: Plugin Architecture

Dynamic plugin loading based on model type:

```python
# plugins/yolo_plugin.py
class YOLOPlugin:
    def load(self, model_id): ...
    def infer(self, model, image): ...

# Main system
def get_plugin(model_id: str) -> Plugin:
    plugin_name = infer_plugin_type(model_id)
    return importlib.import_module(f"plugins.{plugin_name}").Plugin()
```

**Pros**:
- Maximum extensibility
- Can add plugins without core changes

**Cons**:
- Over-engineered for our needs
- Dynamic loading adds complexity
- Harder to type-check and validate

## Consequences

### Positive

1. **Clean Separation**: Each handler owns its model family's logic
2. **Extensibility**: Adding a new model requires one new handler class
3. **Testability**: Each handler can be unit tested in isolation
4. **Single Responsibility**: Handlers only know their model family
5. **Open/Closed**: System is open for extension, closed for modification

### Negative

1. **Indirection**: Multiple layers between API call and inference
2. **Learning Curve**: Developers must understand the pattern
3. **Boilerplate**: New handlers require implementing abstract methods

### Mitigations

- **Indirection**: Clear naming (`Handler`, `Registry`, `Manager`) and this documentation
- **Learning Curve**: This ADR and Academy articles
- **Boilerplate**: Common logic in base class (`_model_to_device`, `bgr_to_pil`)

## Implementation Notes

### Handler Lifecycle

```
Request → ModelManager.load_model()
                ↓
         HandlerRegistry.get_handler(model_id)
                ↓
         handler.load(model_id)
                ↓
         LoadedModel(model, processor, handler)
                ↓
         loaded.infer(image, params)
```

### Key Design Decisions

1. **Processor in tuple**: Some models (YOLO) don't need processors; return `(model, None)`
2. **LoadedModel wrapper**: Hides processor existence from callers
3. **InferenceParams container**: Single parameter object, handlers pick what they need

## References

- [Strategy Pattern - GoF](https://en.wikipedia.org/wiki/Strategy_pattern)
- [Deep Module Principle - Sandi Metz](https://www.sandimetz.com/blog/2016/1/20/design-mendacity-deep-module)
- [Open/Closed Principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)
