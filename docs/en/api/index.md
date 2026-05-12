# API Reference

Complete API documentation for YOLO-Toys.

## Available Protocols

| Protocol | Use Case | Latency |
|----------|----------|---------|
| [REST API](./rest-api) | Single image inference, batch processing | Medium |
| [WebSocket](./websocket) | Real-time video streaming | Low |

## Quick Example

```bash
# REST API
curl -X POST "http://localhost:8000/infer" \
  -F "file=@image.jpg" \
  -F "model=yolov8n.pt"
```

```javascript
// WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');
ws.send(blob); // Send JPEG frame
```
