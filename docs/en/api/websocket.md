# WebSocket Protocol

Real-time streaming protocol for low-latency object detection.

---

## 📋 Overview

WebSocket connections provide the lowest latency for real-time video analysis.

**Endpoint:** `ws://localhost:8000/ws`

---

## 🔌 Connection

### URL Format

```
ws://{host}/ws?model={model_id}&conf={confidence}&iou={iou}
```

### Example Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws?model=yolov8n.pt&conf=0.25');
```

---

## 📤 Client → Server Messages

### Binary Image Frame

Send JPEG-encoded image as binary message:

```javascript
canvas.toBlob((blob) => {
  ws.send(blob);
}, 'image/jpeg', 0.85);
```

### Configuration Update

```javascript
ws.send(JSON.stringify({
  type: 'config',
  conf: 0.5,
  iou: 0.4,
  max_det: 100
}));
```

---

## 📥 Server → Client Messages

### Detection Result

```json
{
  "type": "result",
  "data": {
    "width": 640,
    "height": 480,
    "detections": [
      {
        "bbox": [100.5, 200.3, 250.8, 450.2],
        "score": 0.89,
        "label": "person"
      }
    ],
    "inference_time": 12.5
  }
}
```

---

## 🔗 Related Documentation

- [REST API](./rest-api) — HTTP endpoints reference
- [Architecture](../architecture/overview) — System design
