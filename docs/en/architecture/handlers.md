# Handler Architecture

The handler pattern is the core extensibility mechanism in YOLO-Toys.

## Handler Interface

All handlers implement a common interface:

```python
class BaseHandler:
    def load(self, model_path: str) -> None:
        """Load model from path"""
        pass

    def infer(self, image: np.ndarray, **kwargs) -> dict:
        """Run inference on image"""
        pass

    def unload(self) -> None:
        """Release resources"""
        pass
```

## Existing Handlers

| Handler | Models | Description |
|---------|--------|-------------|
| YOLOHandler | yolov8n, yolov8s, etc. | Ultralytics YOLO models |
| DETRHandler | detr-resnet-50 | Facebook DETR |
| OWLViTHandler | owl-vit-base | OpenAI OWL-ViT |
| GroundingDINOHandler | groundingdino | Grounding DINO |
| BLIPHandler | blip-base | Image captioning & VQA |

## Creating a Custom Handler

```python
from app.handlers.base import BaseHandler

class MyHandler(BaseHandler):
    def load(self, model_path: str) -> None:
        # Load your model here
        self.model = load_my_model(model_path)

    def infer(self, image: np.ndarray, **kwargs) -> dict:
        # Run inference
        results = self.model(image)
        return self.format_results(results)
```

## Handler Registration

Add your handler to the handler registry:

```python
HANDLER_REGISTRY = {
    "yolo": YOLOHandler,
    "detr": DETRHandler,
    "myhandler": MyHandler,  # Your handler
}
```
