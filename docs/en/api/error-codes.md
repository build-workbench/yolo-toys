---
title: Error Codes Reference
---

# Error Codes Reference

This document lists all error conditions and their HTTP status codes.

## HTTP Status Codes

### 200 OK

Request processed successfully.

```json
{
  "width": 640,
  "height": 480,
  "task": "detect",
  "detections": [...],
  "inference_time": 15.3,
  "model": "yolov8n.pt"
}
```

### 400 Bad Request

Invalid request parameters or malformed data.

| Error Message | Cause | Resolution |
|---------------|-------|------------|
| `Invalid image format` | Uploaded file is not a valid image | Upload JPEG, PNG, or WebP |
| `File too large` | Upload exceeds `MAX_UPLOAD_MB` | Compress image or increase limit |
| `Model ID must be a non-empty string` | Empty or null model ID | Provide valid model ID |
| `Invalid model ID: contains forbidden character sequence` | Path traversal attempt | Use alphanumeric model ID |
| `Missing required parameter: question` | VQA endpoint without question | Include `question` parameter |

```json
{
  "detail": "Invalid image format. Supported: JPEG, PNG, WebP"
}
```

### 404 Not Found

Requested resource does not exist.

| Error Message | Cause | Resolution |
|---------------|-------|------------|
| `Model not found: {model_id}` | Unknown model ID | Use model from `/models` endpoint |
| `Unknown model category for {model_id}` | Cannot infer model type | Register model or fix ID |

```json
{
  "detail": "Model not found: unknown-model.pt"
}
```

### 413 Payload Too Large

Upload size exceeds limit.

```json
{
  "detail": "File too large. Maximum: 10MB"
}
```

**Configuration**: Set `MAX_UPLOAD_MB` environment variable.

### 422 Unprocessable Entity

Request validation failed (FastAPI validation).

```json
{
  "detail": [
    {
      "loc": ["query", "conf"],
      "msg": "ensure this value is less than or equal to 1.0",
      "type": "value_error.number.not_le"
    }
  ]
}
```

### 429 Too Many Requests

Rate limit exceeded.

```json
{
  "detail": "Rate limit exceeded. Try again later."
}
```

**Configuration**: Rate limit is `MAX_CONCURRENCY * 60` requests per minute.

### 500 Internal Server Error

Server-side error during processing.

| Error Message | Cause | Resolution |
|---------------|-------|------------|
| `Model inference failed: CUDA out of memory` | GPU memory exhausted | Reduce batch size or use smaller model |
| `ultralytics not installed` | Missing dependency | Install required packages |
| `transformers not installed` | Missing dependency | Install required packages |
| `torch not installed` | Missing dependency | Install required packages |
| `Unexpected inference error` | Unknown error | Check server logs |

```json
{
  "detail": "Model inference failed: CUDA out of memory"
}
```

### 503 Service Unavailable

Service temporarily unavailable (not currently used, reserved for future).

## WebSocket Error Types

WebSocket errors are sent as JSON messages with `type: "error"`:

```json
{
  "type": "error",
  "detail": "Invalid image format"
}
```

| Error Detail | Cause |
|--------------|-------|
| `file too large` | Binary frame exceeds `MAX_UPLOAD_BYTES` |
| `invalid image format` | Cannot decode binary frame as image |
| `Model inference failed: ...` | Inference error |

## Error Handling Implementation

### Decorator Pattern

```python
# app/handlers/error_handling.py
@handle_inference_errors("YOLO")
def _call_model(model, image, kwargs):
    return model(image, **kwargs)
```

The decorator:
1. Catches `RuntimeError` (CUDA OOM, etc.)
2. Logs appropriate error level
3. Re-raises for HTTP layer to handle

### HTTP Layer Handling

```python
# app/api/inference.py
try:
    result = await asyncio.to_thread(model_manager.infer, ...)
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except RuntimeError as e:
    raise HTTPException(status_code=500, detail=f"Model inference failed: {e}")
```

## Logging

Errors are logged with context:

```python
logger.error("YOLO GPU memory exhausted: %s", e)
logger.warning("WebSocket image decode failed")
logger.exception("Unexpected inference error for model %s", model_id)
```

**Log levels**:
- `DEBUG`: Detailed flow information
- `INFO`: Normal operations (model load, cache eviction)
- `WARNING`: Recoverable issues (cache eviction, rate limit)
- `ERROR`: Failures (inference errors, GPU OOM)
- `CRITICAL`: System failures (not currently used)

## Monitoring

Track errors via Prometheus:

```promql
# Error rate by model
sum(rate(inference_requests_total{status="error"}[5m])) by (model)

# Error percentage
sum(rate(inference_requests_total{status="error"}[5m]))
/
sum(rate(inference_requests_total[5m])) * 100
```

## Best Practices

### Client-Side Handling

```python
import requests

try:
    response = requests.post("/infer", files={"file": image})
    response.raise_for_status()
    return response.json()
except requests.HTTPStatusError as e:
    if e.response.status_code == 400:
        print("Invalid request:", e.response.json()["detail"])
    elif e.response.status_code == 404:
        print("Model not found")
    elif e.response.status_code == 500:
        print("Server error, retry later")
```

### Retry Strategy

For transient errors (500, 429):

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(HTTPStatusError)
)
def infer_with_retry(image):
    response = requests.post("/infer", files={"file": image})
    response.raise_for_status()
    return response.json()
```
