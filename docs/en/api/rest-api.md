# REST API Reference

Complete reference for YOLO-Toys HTTP API endpoints.

---

## 📋 Overview

Base URL: `http://localhost:8000`

All API responses are in JSON format. Errors follow the standard HTTP status code convention.

---

## 🔍 Endpoints

### Health Check

Check server status and system information.

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "version": "3.1.0",
  "device": "cuda:0",
  "default_model": "yolov8n.pt"
}
```

---

### List Models

Get all available models grouped by category.

```http
GET /models
```

---

### Single Image Inference

Perform inference on a single image.

```http
POST /infer
```

**Content-Type:** `multipart/form-data`

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `file` | File | Yes | - | Image file (JPEG, PNG, WEBP) |
| `model` | string | No | `yolov8n.pt` | Model identifier |
| `conf` | float | No | 0.25 | Confidence threshold (0.0-1.0) |
| `iou` | float | No | 0.45 | IoU threshold for NMS |

**Response (200 OK):**
```json
{
  "width": 640,
  "height": 480,
  "task": "detect",
  "detections": [
    {
      "bbox": [100.5, 200.3, 250.8, 450.2],
      "score": 0.89,
      "label": "person"
    }
  ],
  "inference_time": 12.5,
  "model": "yolov8n.pt"
}
```

---

### Image Captioning

Generate automatic description for an image.

```http
POST /caption
```

**Response:**
```json
{
  "caption": "a person riding a skateboard on a street",
  "inference_time": 120.5
}
```

---

### Visual Question Answering

Answer questions about an image.

```http
POST /vqa
```

**Response:**
```json
{
  "answer": "blue",
  "inference_time": 95.2,
  "question": "What color is the car?"
}
```

---

## 🚦 Error Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input parameters |
| 404 | Not Found | Model or resource not found |
| 500 | Internal Server Error | Server processing error |

---

## 🔗 Next Steps

- [WebSocket Protocol](./websocket) — Real-time streaming API
- [Architecture](../architecture/overview) — System design overview
- [Models](../reference/models) — Supported model reference
