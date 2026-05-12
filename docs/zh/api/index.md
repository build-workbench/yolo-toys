# API 参考

YOLO-Toys 完整 API 文档。

## 可用协议

| 协议 | 适用场景 | 延迟 |
|----------|---------|---------|
| [REST API](./rest-api) | 单图推理、批处理 | 中等 |
| [WebSocket](./websocket) | 实时视频流 | 低 |

## 快速示例

```bash
# REST API
curl -X POST "http://localhost:8000/infer" \
  -F "file=@image.jpg" \
  -F "model=yolov8n.pt"
```

```javascript
// WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');
ws.send(blob); // 发送 JPEG 帧
```
