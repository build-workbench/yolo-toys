# 快速开始指南

在 5 分钟内启动 YOLO-Toys 并完成你的第一次目标检测。

---

## 🚀 启动服务器

### Python 原生方式

```bash
# 确保已激活虚拟环境
source .venv/bin/activate  # Linux/macOS

# 启动服务器（自动重载）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

你应该看到类似输出：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Docker 方式

```bash
docker-compose up -d
```

---

## 🌐 访问 Web 界面

1. 打开浏览器访问：`http://localhost:8000`

2. **授权摄像头**：提示时允许摄像头访问以进行实时检测。

3. **选择模型**：从下拉菜单中选择：
   - `yolov8n.pt` — 最快，适合测试
   - `yolov8s.pt` — 速度/精度平衡
   - `yolov8m.pt` — 更高精度，较慢

4. **调整设置**（可选）：
   - **置信度**：0.25（默认）— 值越低检测到的对象越多
   - **IoU**：0.45 — 重叠框的 NMS 阈值
   - **最大检测数**：300 — 每帧最大对象数

5. **点击「开始检测」** 开始实时目标检测！

---

## 🔌 使用 WebSocket 流式传输

最低延迟的实时检测，使用 WebSocket 流式传输：

### JavaScript 示例

```javascript
const ws = new WebSocket('ws://localhost:8000/ws?model=yolov8n.pt&conf=0.25');

ws.onopen = () => {
  console.log('WebSocket 已连接');
};

ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  console.log('检测结果:', result.detections);
  console.log('推理时间:', result.inference_time, 'ms');
};

// 发送图像帧（JPEG 二进制）
function sendFrame(imageBlob) {
  ws.send(imageBlob);
}
```

### 更新配置

无需重新连接即可更新检测参数：

```javascript
ws.send(JSON.stringify({
  type: 'config',
  conf: 0.5,      // 新置信度阈值
  iou: 0.4,       // 新 IoU 阈值
  max_det: 100    // 新最大检测数
}));
```

---

## 📡 REST API 示例

### 单图推理

使用 cURL：

```bash
curl -X POST "http://localhost:8000/infer" \
  -F "file=@image.jpg" \
  -F "model=yolov8n.pt" \
  -F "conf=0.25" \
  -F "iou=0.45"
```

使用 Python (requests)：

```python
import requests

url = "http://localhost:8000/infer"
files = {"file": open("image.jpg", "rb")}
data = {"model": "yolov8n.pt", "conf": 0.25}

response = requests.post(url, files=files, data=data)
result = response.json()

print(f"检测到 {len(result['detections'])} 个对象")
for det in result['detections']:
    print(f"  - {det['label']}: {det['score']:.2f}")
```

### 响应格式

```json
{
  "width": 640,
  "height": 480,
  "task": "detect",
  "detections": [
    {
      "bbox": [100.5, 200.3, 150.8, 350.2],
      "score": 0.89,
      "label": "person"
    }
  ],
  "inference_time": 5.2,
  "model": "yolov8n.pt"
}
```

---

## ✅ 下一步？

- [API 参考](../api/rest-api) — 完整 API 文档
- [架构](../architecture/overview) — 了解系统设计
- [部署](../deployment/docker) — 生产环境部署指南
- [支持的模型](../reference/models) — 模型规格说明
