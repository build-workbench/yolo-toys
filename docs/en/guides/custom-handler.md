---
title: Custom Handler Development Guide
---

# Custom Handler Development Guide

This guide walks you through creating a custom handler to support a new model family.

## Overview

A handler is responsible for:
1. Loading the model (and optional processor)
2. Preprocessing inputs
3. Running inference
4. Postprocessing outputs

All handlers inherit from `BaseHandler` and implement two abstract methods.

## Step-by-Step Guide

### Step 1: Define the Category

Add a new category to `ModelCategory` enum:

```python
# app/models_metadata.py
class ModelCategory(Enum):
    ...
    MY_NEW_TASK = auto()  # Add this

    @property
    def display_name(self) -> str:
        names = {
            ...
            self.MY_NEW_TASK: "My New Task",
        }
        return names.get(self, str(self))
```

### Step 2: Create the Handler

Create a new file `app/handlers/my_handler.py`:

```python
"""
My custom model handler
"""

import time
from typing import Any

import numpy as np

from app.handlers.base import BaseHandler
from app.handlers.error_handling import handle_inference_errors
from app.params import InferenceParams


class MyHandler(BaseHandler):
    """Handler for my custom model family."""

    def _do_load(self, model_id: str) -> tuple[Any, Any | None]:
        """
        Load model and optional processor.

        Args:
            model_id: Model identifier (e.g., "my-org/my-model")

        Returns:
            Tuple of (model, processor). Processor can be None.
        """
        # Example: Load from HuggingFace
        from transformers import AutoModel, AutoProcessor

        processor = AutoProcessor.from_pretrained(model_id)
        model = AutoModel.from_pretrained(model_id)
        model = self._model_to_device(model)  # Move to GPU if needed

        return model, processor

    def _infer_impl(
        self,
        model: Any,
        processor: Any | None,
        image: np.ndarray,
        params: InferenceParams,
    ) -> dict[str, Any]:
        """
        Execute inference.

        Args:
            model: Loaded model object
            processor: Loaded processor (or None)
            image: Input image (BGR numpy array)
            params: Inference parameters

        Returns:
            Result dictionary with required fields
        """
        t0 = time.time()

        # Preprocess
        pil_image = self.bgr_to_pil(image)  # Convert BGR → RGB PIL
        inputs = processor(images=pil_image, return_tensors="pt")
        inputs = self._to_device(inputs)  # Move tensors to GPU

        # Inference
        with torch.no_grad():
            outputs = self._call_model(model, inputs)

        # Postprocess
        results = self._process_outputs(outputs, params)

        elapsed = (time.time() - t0) * 1000.0

        return self.make_result(
            image,
            detections=results,
            inference_time=elapsed,
            task="my_task"
        )

    @staticmethod
    @handle_inference_errors("MyModel")
    def _call_model(model: Any, inputs: dict) -> Any:
        """Wrapped model call with error handling."""
        return model(**inputs)

    def _process_outputs(self, outputs, params) -> list[dict]:
        """Convert model outputs to standard detection format."""
        # Implement your postprocessing logic
        detections = []
        # ... parse outputs ...
        return detections
```

### Step 3: Register the Handler

Add to the category-handler mapping:

```python
# app/handlers/registry.py
from app.handlers.my_handler import MyHandler

_CATEGORY_HANDLER_MAP = {
    ...
    ModelCategory.MY_NEW_TASK: MyHandler,
}
```

### Step 4: Add Category Inference Logic

Update `infer_from_id` to recognize your models:

```python
# app/models_metadata.py
@classmethod
def infer_from_id(cls, model_id: str, registry: dict | None = None):
    ...
    # Add pattern matching
    lower = model_id.lower()
    if "my-model" in lower or "myorg" in lower:
        return cls.MY_NEW_TASK
    ...
```

### Step 5: Add Model Metadata

Register specific models:

```python
# app/models_metadata.py
MODEL_REGISTRY["my-org/my-model-v1"] = {
    "category": ModelCategory.MY_NEW_TASK,
    "name": "My Model v1",
    "description": "Description of my model",
    "speed": "medium",
    "accuracy": "high",
}
```

### Step 6: Add Custom Parameters (Optional)

If your model needs unique parameters:

```python
# app/params.py
@dataclass
class InferenceParams:
    ...
    my_custom_param: float = 1.0

    def for_my_model(self) -> dict[str, Any]:
        return {
            "custom_param": self.my_custom_param,
        }
```

### Step 7: Write Tests

```python
# tests/test_my_handler.py
import pytest
import numpy as np

from app.handlers.my_handler import MyHandler
from app.params import InferenceParams


@pytest.fixture
def handler():
    return MyHandler(device="cpu")


def test_handler_loads_model(handler):
    """Test model loading."""
    loaded = handler.load("my-org/my-model-v1")
    assert loaded.model_id == "my-org/my-model-v1"
    assert loaded.model is not None


def test_handler_infers(handler):
    """Test inference produces valid output."""
    loaded = handler.load("my-org/my-model-v1")
    dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)

    result = loaded.infer(dummy_image, InferenceParams())

    assert "width" in result
    assert "height" in result
    assert "inference_time" in result
    assert result["task"] == "my_task"


def test_handler_handles_errors(handler):
    """Test error handling."""
    loaded = handler.load("my-org/my-model-v1")

    # Should raise, not crash
    with pytest.raises(RuntimeError):
        # Force an error condition
        ...
```

## Common Patterns

### No Processor Needed

Some models (like YOLO) don't need a separate processor:

```python
def _do_load(self, model_id: str) -> tuple[Any, None]:
    model = load_my_model(model_id)
    return model, None  # Processor is None
```

### Device Management

Use inherited methods for device handling:

```python
# Move model to GPU
model = self._model_to_device(model)

# Move input tensors
inputs = self._to_device(inputs)

# Optional: specify different device
inputs = self._to_device(inputs, device="cuda:1")
```

### Image Conversion

```python
# BGR numpy → RGB PIL
pil_image = self.bgr_to_pil(image)

# If you need grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

### Result Formatting

Use the helper function:

```python
return self.make_result(
    image,                          # For width/height extraction
    detections=detections,          # List of detection dicts
    inference_time=elapsed_ms,      # Float, milliseconds
    task="detect",                  # Task type string
    # Additional fields...
    caption="A cat sitting on a chair",  # For captioning
    answer="Yes",                        # For VQA
    text_queries=["cat", "dog"],         # For open-vocab
)
```

## Best Practices

### 1. Use Error Decorator

```python
@staticmethod
@handle_inference_errors("MyModel")
def _call_model(model, inputs):
    return model(**inputs)
```

This provides consistent error logging and propagation.

### 2. Log Appropriately

```python
import logging
logger = logging.getLogger(__name__)

# Debug: Detailed flow
logger.debug("Processing batch of %d items", len(batch))

# Info: Normal operations
logger.info("Model loaded: %s", model_id)

# Warning: Recoverable issues
logger.warning("Low confidence detections: %d", low_conf_count)

# Error: Failures (usually in decorator)
```

### 3. Time Operations

```python
t0 = time.time()
# ... operation ...
elapsed = (time.time() - t0) * 1000.0  # Milliseconds
```

### 4. Handle Edge Cases

```python
def _process_outputs(self, outputs, params):
    # Empty results
    if outputs is None:
        return []

    # Low confidence filtering
    detections = [
        d for d in raw_detections
        if d["score"] >= params.conf
    ]

    # Max detections limit
    if len(detections) > params.max_det:
        detections = sorted(detections, key=lambda x: -x["score"])[:params.max_det]

    return detections
```

## Troubleshooting

### Import Errors

```
RuntimeError: transformers not installed
```

**Solution**: Add to requirements or handle gracefully:

```python
try:
    from transformers import AutoModel
except ImportError as exc:
    raise RuntimeError("transformers not installed") from exc
```

### CUDA Out of Memory

```
RuntimeError: CUDA out of memory
```

**Solutions**:
1. Use smaller batch size
2. Use smaller model
3. Enable half-precision: `params.half = True`
4. Clear cache: `model_manager.clear_cache()`

### Shape Mismatch

```
RuntimeError: Expected 3D input, got 4D
```

**Solution**: Check preprocessing matches model expectations.

## Example: SAM Handler

Here's a complete example for Segment Anything Model:

```python
class SAMHandler(BaseHandler):
    """Segment Anything Model handler."""

    def _do_load(self, model_id: str) -> tuple[Any, Any]:
        from segment_anything import sam_model_registry, SamPredictor

        # Parse model type from ID
        model_type = "vit_h" if "huge" in model_id else "vit_l"

        sam = sam_model_registry[model_type](checkpoint=model_id)
        sam = self._model_to_device(sam)
        predictor = SamPredictor(sam)

        return predictor, sam

    def _infer_impl(self, predictor, sam, image, params) -> dict:
        t0 = time.time()

        # SAM expects RGB
        rgb_image = image[:, :, ::-1]
        predictor.set_image(rgb_image)

        # Example: automatic mask generation
        masks, scores, _ = predictor.predict(
            point_coords=None,
            box=None,
            multimask_output=True
        )

        # Format results
        detections = [
            {"mask": mask.tolist(), "score": float(score)}
            for mask, score in zip(masks, scores)
        ]

        elapsed = (time.time() - t0) * 1000.0
        return self.make_result(
            image, detections=detections,
            inference_time=elapsed, task="segment"
        )
```
