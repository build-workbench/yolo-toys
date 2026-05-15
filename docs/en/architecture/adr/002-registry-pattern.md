---
title: ADR-002 - Centralized Registry over Distributed Metadata
---

# ADR-002: Centralized Registry over Distributed Metadata

| Status | Date | Decision Makers |
|--------|------|-----------------|
| Accepted | 2024-01-15 | Architecture Team |

## Context

YOLO-Toys needs to:
1. Know what models are available
2. Map model IDs to handlers
3. Display model metadata in API responses
4. Infer categories for unknown models

We had several options for organizing this information:
- Central registry constant
- Metadata distributed across handlers
- Configuration files (YAML, JSON)
- External database

## Decision

We adopted a **Centralized Registry Pattern** where:
- `MODEL_REGISTRY` is a single dict constant
- `ModelCategory` enum encapsulates all categories
- Category inference logic lives in `ModelCategory.infer_from_id()`

```python
# Single source of truth
MODEL_REGISTRY: dict[str, dict[str, Any]] = {
    "yolov8n.pt": {
        "category": ModelCategory.YOLO_DETECT,
        "name": "YOLOv8 Nano",
        "description": "Ultra-lightweight detection model",
        "speed": "extreme fast",
        "accuracy": "medium",
    },
    ...
}
```

## Alternatives Considered

### Alternative 1: Distributed Metadata

Store metadata alongside each handler:

```python
class YOLOHandler(BaseHandler):
    MODELS = {
        "yolov8n.pt": {"name": "YOLOv8 Nano", ...},
        "yolov8s.pt": {"name": "YOLOv8 Small", ...},
    }

    @classmethod
    def get_models(cls):
        return cls.MODELS

class DETRHandler(BaseHandler):
    MODELS = {
        "facebook/detr-resnet-50": {...},
    }

# To get all models
all_models = {}
for handler in [YOLOHandler, DETRHandler, ...]:
    all_models.update(handler.get_models())
```

**Pros**:
- Co-locates model info with inference logic
- Handler authors own their models

**Cons**:
- Hard to enumerate all models (need to import all handlers)
- Category information scattered
- Difficult to maintain consistency
- Circular import risks

### Alternative 2: Configuration Files

Store metadata in YAML/JSON:

```yaml
# models.yaml
models:
  yolov8n.pt:
    category: yolo_detect
    name: YOLOv8 Nano
    handler: YOLOHandler
  facebook/detr-resnet-50:
    category: hf_detr
    name: DETR ResNet-50
    handler: DETRHandler
```

**Pros**:
- Easy to edit without touching code
- Can be validated with schema
- Supports runtime updates (reload config)

**Cons**:
- Separation from code (drift risk)
- No type safety
- Need to load and parse at startup
- Harder to version control changes

### Alternative 3: External Database

Store metadata in PostgreSQL/Redis:

```sql
CREATE TABLE models (
    id VARCHAR PRIMARY KEY,
    category VARCHAR,
    name VARCHAR,
    handler VARCHAR,
    ...
);
```

**Pros**:
- Dynamic updates without restart
- Query flexibility
- Can store usage statistics

**Cons**:
- Operational complexity
- Network dependency at startup
- Overkill for static metadata
- Need migration management

### Alternative 4: Automatic Discovery

Scan filesystem/HuggingFace Hub:

```python
def discover_models():
    models = {}
    # Scan .pt files
    for path in Path("models").glob("*.pt"):
        models[path.name] = infer_metadata(path)
    # Query HuggingFace API
    for model_id in get_popular_vision_models():
        models[model_id] = fetch_hf_metadata(model_id)
    return models
```

**Pros**:
- Always up-to-date
- No manual maintenance

**Cons**:
- Startup latency (network calls)
- Non-deterministic results
- Hard to customize metadata
- Requires network access

## Consequences

### Positive

1. **Single Source of Truth**: All metadata in one place
2. **Type Safety**: Enum for categories, typed dicts
3. **Predictable**: Same models available every run
4. **Simple**: Dict lookup, no external dependencies
5. **Version Controlled**: Changes tracked in git

### Negative

1. **Centralized Changes**: Adding models requires code change
2. **Memory Overhead**: Registry always in memory
3. **No Runtime Updates**: Adding models requires restart

### Mitigations

- **Centralized Changes**: Simple dict structure, PRs easy to review
- **Memory Overhead**: Negligible (few KB)
- **No Runtime Updates**: Support ad-hoc `.pt` files via inference

## Implementation Notes

### Registry Structure

```python
MODEL_REGISTRY: dict[str, dict[str, Any]] = {
    model_id: {
        "category": ModelCategory,    # Required: enum value
        "name": str,                  # Display name
        "description": str,           # Human description
        "speed": str,                 # Qualitative speed
        "accuracy": str,              # Qualitative accuracy
    }
}
```

### Category Inference Strategy

```python
@classmethod
def infer_from_id(cls, model_id: str, registry: dict | None = None):
    # Priority 1: Explicit registry lookup
    if registry and model_id in registry:
        return registry[model_id]["category"]

    # Priority 2: File extension patterns
    if model_id.endswith(".pt"):
        return cls._infer_yolo_variant(model_id)

    # Priority 3: String patterns
    # Priority 4: Fallback heuristics
```

### API Usage

```python
# List all models
models = get_available_models()
# → {"yolo_detect": {"name": "...", "models": [...]}, ...}

# Get specific model
info = get_model_info("yolov8n.pt")
# → {"category": ..., "name": ..., ...}

# Resolve handler
registry = HandlerRegistry(device)
handler = registry.get_handler("yolov8n.pt")
```

## References

- [Registry Pattern](https://martinfowler.com/eaaCatalog/registry.html)
- [Single Source of Truth](https://en.wikipedia.org/wiki/Single_source_of_truth)
