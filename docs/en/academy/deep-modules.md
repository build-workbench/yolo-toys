---
title: Deep Modules Design Philosophy
---

# Deep Modules Design Philosophy

One of the most important architectural decisions in YOLO-Toys is the use of "Deep Modules" — interfaces that hide significant complexity behind simple facades. This pattern is derived from [Clean Architecture](/en/citations) principles and enables the system's maintainability.

## The Deep Module Principle

> "The best modules are those whose interfaces are much simpler than their implementations."

A module is "deep" when:
- **Interface**: Simple, focused, easy to understand
- **Implementation**: Complex, handles many concerns

```
┌─────────────────────────────────────────────────────────────┐
│                      Deep Module                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Simple Interface                     │  │
│  │         load(model_id) → LoadedModel                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Complex Implementation                │  │
│  │  • Security validation                                  │  │
│  │  • Registry lookup                                      │  │
│  │  • Cache hit/miss handling                             │  │
│  │  • Memory pressure management                           │  │
│  │  • CUDA cache clearing                                  │  │
│  │  • Thread-safe access                                   │  │
│  │  • Handler instantiation                                │  │
│  │  • Model warmup                                         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Primary Examples in YOLO-Toys

### `LoadedModel` Wrapper

The `LoadedModel` class is the quintessential deep module:

```python
class LoadedModel:
    """A loaded model with its processor and metadata."""
    model: Any
    processor: Any | None
    handler: BaseHandler
    loaded_at: datetime

    # Callers see:
    def infer(self, image: bytes, params: InferenceParams) -> dict:
        """Execute inference on the loaded model."""
        # Internally handles:
        # - Image preprocessing (handler-specific)
        # - Parameter marshaling (model-specific)
        # - Output normalization
        # - Error handling
        # - Timing metrics
```

**What callers see**: A simple `infer(image, params)` method.

**What it hides**:
- Handler dispatch logic
- Image preprocessing pipelines
- Model-specific parameter extraction
- Output format normalization
- Performance timing
- Error recovery

### `InferenceParams` Dataclass

```python
@dataclass
class InferenceParams:
    """Inference parameters with model-specific extraction."""
    conf: float = 0.25
    iou: float = 0.45
    max_det: int = 300
    device: str = "auto"
    imgsz: int = 640
    half: bool = False
    text_queries: str | None = None
    question: str | None = None

    def for_yolo(self) -> dict:
        """Extract YOLO-specific parameters."""
        return {
            "conf": self.conf,
            "iou": self.iou,
            "max_det": self.max_det,
            "device": self.device,
            "imgsz": self.imgsz,
            "half": self.half,
        }

    def for_detr(self) -> dict:
        """Extract DETR-specific parameters."""
        return {
            "device": self.device,
            # DETR doesn't use conf, iou, etc.
        }
```

**What callers see**: A dataclass with sensible defaults.

**What it hides**:
- Parameter validation logic
- Model-specific parameter subsets
- Default value management
- Type conversion

### `ModelManager` Control Plane

```python
class ModelManager:
    """The runtime's control plane."""

    def infer(self, model_id: str, image: bytes, **kwargs) -> dict:
        """The single entry point for all inference."""
        # Callers see: one method
        # Internally: security check, cache lookup, handler dispatch,
        #             memory management, metrics collection, error handling
```

**What callers see**: `infer(model_id, image, **kwargs)`

**What it hides**:
- Security validation (path traversal, magic numbers)
- Cache hit/miss decision tree
- LRU eviction under memory pressure
- Handler registry lookup
- Thread-safe model loading
- Prometheus metrics recording

## Why Deep Modules Matter

### 1. Cognitive Load Reduction

Shallow modules require callers to understand implementation details:

```python
# Without deep modules (shallow)
model = registry.lookup(model_id)
handler = handler_factory.create(model.category)
params = handler.extract_params(kwargs)
image = handler.preprocess(image)
result = handler.infer(model, image, params)
output = handler.postprocess(result)
```

```python
# With deep modules
result = manager.infer(model_id, image, **kwargs)
```

### 2. Change Isolation

When implementation changes, callers don't need to update:

```python
# Adding a new model family only requires:
# 1. New handler class
# 2. Registry entry
# All existing callers continue to work
```

### 3. Testing Simplicity

Deep modules have clear boundaries for mocking:

```python
# Test just needs to mock the simple interface
def test_detection(monkeypatch):
    def fake_infer(model_id, image, **kwargs):
        return {"detections": [...]}
    monkeypatch.setattr(manager, "infer", fake_infer)
```

## Anti-Pattern: Shallow Modules

Shallow modules expose implementation details:

```python
# Anti-pattern: Everything is public
class ModelManagerShallow:
    def __init__(self):
        self.cache = ModelCache()      # Exposed!
        self.registry = HandlerRegistry()  # Exposed!
        self.handlers = {}             # Exposed!

    # Callers must understand all of these
    def get_cache_stats(self): ...
    def register_handler(self, category, handler): ...
    def load_model_direct(self, model_id): ...
    def check_memory(self): ...
    def clear_cuda_cache(self): ...
```

This leads to:
- **Coupling**: Callers depend on internal structure
- **Fragility**: Changes break callers
- **Complexity**: Everyone must understand everything

## The Interface Cost Principle

Every public interface has a cost:

- **Documentation cost**: Every public method needs docs
- **Testing cost**: Every public method needs tests
- **Maintenance cost**: Every public method is a constraint
- **Learning cost**: Every public method must be learned

Deep modules minimize interface surface while maximizing functionality.

## Practical Guidelines

### 1. Start with the Interface

Write the call site first:

```python
# What would I want to write?
result = manager.infer("yolov8n.pt", image, conf=0.5)
```

Then implement to make that interface possible.

### 2. Hide Infrastructure

Callers shouldn't know about:
- Caching implementation
- Threading details
- Resource management
- Logging mechanisms

### 3. Facade Complex Subsystems

If a subsystem has 10 classes, create one facade:

```python
# Instead of exposing 10 classes
model_cache = ModelCache(...)
handler_registry = HandlerRegistry(...)
security_validator = SecurityValidator(...)
# ... 7 more

# Expose one facade
manager = ModelManager(...)  # Internally uses all of the above
```

### 4. Parameter Objects over Many Parameters

```python
# Shallow: 8 parameters
def infer(model_id, image, conf, iou, max_det, device, imgsz, half):
    ...

# Deep: 1 parameter object with defaults
def infer(model_id, image, params=None):
    params = params or InferenceParams()
    ...
```

## References

<CitationBlock :number="1" authors="Martin, Robert C." title="Clean Architecture: A Craftsman's Guide to Software Structure and Design" venue="Prentice Hall" year="2017" />

<CitationBlock :number="2" authors="Parnas, David L." title="On the Criteria to Be Used in Decomposing Systems into Modules" venue="Communications of the ACM" year="1972" />

## What to Read Next

<CrossReference href="/en/academy/handler-pattern" section="Academy" label="Handler Pattern" />
<CrossReference href="/en/architecture/overview" section="Architecture" label="System Overview" />
