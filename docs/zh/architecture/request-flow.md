---
title: 请求流程
---

# 请求流程

本文档详细描述 YOLO-Toys 的请求处理流程。

## 整体流程

```mermaid
sequenceDiagram
    participant C as 客户端
    participant API as FastAPI
    participant MM as ModelManager
    participant Cache as ModelCache
    participant H as Handler
    participant M as Model

    C->>API: POST /infer {file, model}
    API->>MM: infer(model_id, image, params)

    alt 模型在缓存中
        MM->>Cache: cache[model_id]
        Cache-->>MM: LoadedModel
    else 模型未缓存
        MM->>H: load(model_id)
        H->>M: 加载模型权重
        M-->>H: 模型就绪
        H-->>MM: LoadedModel
        MM->>Cache: cache[model_id] = LoadedModel
    end

    MM->>H: infer(image, params)
    H->>M: 前向传播
    M-->>H: 原始结果
    H-->>MM: 格式化结果
    MM-->>API: 结果字典
    API-->>C: JSON 响应

    Note over Cache: TTL 自动过期<br/>内存压力时 LRU 驱逐
```

## REST API 流程

### 1. 请求接收

```python
@app.post("/infer")
async def infer(
    file: UploadFile = File(...),
    model: str = Form(...),
    confidence: float = Form(0.25),
):
    # 读取图片
    image = await file.read()

    # 调用 ModelManager
    result = await model_manager.infer(model, image, params)

    return result
```

### 2. 模型加载

1. 检查缓存是否存在模型
2. 如不存在，从 HandlerRegistry 获取 Handler
3. 调用 Handler.load() 加载模型
4. 将 LoadedModel 存入缓存

### 3. 推理执行

1. 从缓存获取 LoadedModel
2. 调用 LoadedModel.infer()
3. 处理结果格式化
4. 返回 JSON 响应

## WebSocket 流程

```mermaid
sequenceDiagram
    participant C as 客户端
    participant WS as WebSocket
    participant MM as ModelManager

    C->>WS: 连接 /ws
    WS-->>C: 连接确认

    loop 推理循环
        C->>WS: 发送图片 + 参数
        WS->>MM: infer()
        MM-->>WS: 结果
        WS-->>C: 推送结果
    end

    C->>WS: 关闭连接
    WS-->>C: 连接关闭
```

## 性能关键路径

| 阶段 | 耗时 | 优化点 |
|------|------|--------|
| 图片解码 | ~5ms | 使用 libjpeg-turbo |
| 模型推理 | ~30ms | FP16、批处理 |
| 结果序列化 | ~2ms | 使用 orjson |

## 错误处理流程

所有错误在 API 层统一捕获并转换为标准错误响应格式。
