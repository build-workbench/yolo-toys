# Handler Architecture

The handler pattern is the core extensibility mechanism in YOLO-Toys. It is the boundary that keeps model-family-specific logic from leaking into routes, caching, and transport concerns.

## Handler interface

All handlers inherit from `BaseHandler` and implement two abstract methods:

```python
class BaseHandler(ABC):
    def load(self, model_id: str) -> LoadedModel:
        """Load model, return a LoadedModel wrapper."""
        model, processor = self._do_load(model_id)
        return LoadedModel(model, processor, self, model_id)

    @abstractmethod
    def _do_load(self, model_id: str) -> tuple[Any, Any | None]:
        """Family-specific model loading."""

    @abstractmethod
    def _infer_impl(self, model, processor, image, params) -> dict[str, Any]:
        """Family-specific inference."""
```

The `LoadedModel` wrapper is a **Deep Module** [^1]: it hides the existence of `processor` from callers and exposes a single `infer(image, params)` method. This means a route handler never needs to know whether a model has a separate processor or not.

## Existing handlers

| Handler | Category | Models | Key dependency |
|---------|----------|--------|---------------|
| `YOLOHandler` | YOLO | yolov8n, yolov8s, yolov8m, yolov8l, yolov8x | `ultralytics.YOLO` |
| `DETRHandler` | DETR | facebook/detr-resnet-50, facebook/detr-resnet-101 | `transformers.DetrForObjectDetection` |
| `OWLViTHandler` | Open-vocabulary | google/owlvit-base-patch32 | `transformers.OwlViTForObjectDetection` |
| `GroundingDINOHandler` | Grounded detection | IDEA-Research/grounding-dino-tiny | `transformers` pipeline |
| `BLIPCaptionHandler` | Captioning | Salesforce/blip-image-captioning-base | `transformers.BlipForConditionalGeneration` |
| `BLIPVQAHandler` | Visual QA | Salesforce/blip-vqa-base | `transformers.BlipForQuestionAnswering` |

## Creating a custom handler

```python
from app.handlers.base import BaseHandler, LoadedModel
from app.params import InferenceParams

class RTDETRHandler(BaseHandler):
    def _do_load(self, model_id: str) -> tuple[Any, None]:
        model = transformers.RTDetrForObjectDetection.from_pretrained(model_id)
        model = self._model_to_device(model)
        return model, None

    def _infer_impl(self, model, processor, image, params: InferenceParams) -> dict[str, Any]:
        inputs = self._preprocess(image)
        outputs = model(**inputs)
        return self._postprocess(outputs)
```

Register it:

```python
from app.handlers.registry import _CATEGORY_HANDLER_MAP
from app.models_metadata import ModelCategory

_CATEGORY_HANDLER_MAP[ModelCategory.HF_RT_DETR] = RTDETRHandler
```

## Handler registration and caching

The `HandlerRegistry` caches handler **instances** (not models) by class name:

```python
class HandlerRegistry:
    def get_handler(self, model_id: str) -> BaseHandler:
        category = self._resolve_category(model_id)
        handler_cls = _CATEGORY_HANDLER_MAP.get(category)
        if handler_cls.__name__ not in self._handler_cache:
            self._handler_cache[handler_cls.__name__] = handler_cls(self._config_or_device)
        return self._handler_cache[handler_cls.__name__]
```

This means that if 10 different YOLO models are loaded, only **one** `YOLOHandler` instance exists. The handler instance is stateless with respect to model identity; it only needs the device/config to know where to run inference.

## Device abstraction

Handlers do not hardcode device placement. The `BaseHandler` base class provides:

```python
def _model_to_device(self, model: Any) -> Any:
    if self._device != "cpu" and hasattr(model, "to"):
        model = model.to(self._device)
    return model

def _to_device(self, inputs: dict[str, Any], device: str | None = None) -> dict[str, Any]:
    target = device or self._device
    if target == "cpu":
        return inputs
    return {k: (v.to(target) if hasattr(v, "to") else v) for k, v in inputs.items()}
```

This allows handlers to work on CPU, CUDA, or Apple Silicon (MPS) without code changes.

## What to read next

- [Handler Pattern](/en/academy/handler-pattern) for the design essay
- [Registry Pattern](/en/academy/registry-pattern) for dispatch reasoning
- [Caching Strategy](/en/academy/caching-strategy) for how loaded models are cached
- [Evolution](/en/research/evolution) for how the handler boundary emerged from flat endpoints

[^1]: Martin, Robert C. *Clean Architecture*. Prentice Hall, 2017.
