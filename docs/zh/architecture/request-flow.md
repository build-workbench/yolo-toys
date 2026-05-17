# 请求生命周期

本页追踪一次推理请求在运行时中的完整路径。生命周期之所以重要，是因为公共 API 的质量取决于系统在哪里进行转换、缓存、校验和格式化。

<FigureFrame
  title="图 2. 端到端生命周期"
  caption="请求通过传输特定的表面进入，但在模型特定执行开始之前，会汇聚到单一的协调路径上。"
>
  <ThemeAwareSvg src="/images/request-lifecycle.svg" alt="YOLO-Toys request lifecycle" title="Request Lifecycle" />
</FigureFrame>

## 分步路径

1. **入口**：请求通过 HTTP 或 WebSocket 进入。
2. **校验**：参数、文件和模型标识符在执行开始前被检查。
3. **协调**：`ModelManager` 选择或复用模型实例，并解析 handler。
4. **执行**：选定的 handler 运行模型家族特有的推理。
5. **归一化**：原始输出被整形为稳定的响应契约。
6. **输出**：运行时返回 JSON 或流式帧级载荷。

## 入口与传输抽象

运行时支持两种主要入口表面：

- **HTTP REST API**（`/infer`、`/caption`、`/vqa`、`/models`、`/labels`、`/metrics`、`/health`）
- **WebSocket**（`/ws`），用于实时帧流

两种表面共享相同的底层推理管道。WebSocket handler 用帧级流式逻辑包裹 HTTP 路径，因此核心执行代码不会分叉。

### WebSocket 帧协议

WebSocket 端点期望每帧一个 JSON 消息：

```json
{
  "model_id": "yolov8n.pt",
  "image": "base64-encoded-image-data",
  "conf": 0.25,
  "iou": 0.45,
  "max_det": 300
}
```

响应以带有 `frame_id` 和 `results` 数组的 JSON 对象流式传输，无需轮询即可实现实时可视化。

## 校验与参数整形

在接触任何模型之前，运行时通过 Pydantic schema 校验请求：

```python
class InferenceParams(BaseModel):
    conf: float = Field(default=0.25, ge=0.0, le=1.0)
    iou: float = Field(default=0.45, ge=0.0, le=1.0)
    max_det: int = Field(default=300, ge=1, le=1000)
    device: str | None = None
    imgsz: int | None = None
    half: bool = False
    text_queries: list[str] | None = None
    question: str | None = None
```

该参数对象**贯穿整个栈**，从路由 handler 到 `ModelManager` 再到 `BaseHandler._infer_impl()`，确保每个边界上的类型安全。

## 为什么归一化位于执行之后

上游模型在输出形状、标签语义、置信度行为和辅助产物上存在分歧。如果路由 handler 试图直接归一化这些差异，传输层就会成为模型语义堆积的地方。YOLO-Toys 的做法是保持路由表面轻薄，让 handler 和 formatter helper 执行翻译工作。

### 归一化契约

每个 handler 返回一个具有保证 schema 的字典：

```python
{
    "model_id": str,
    "inference_time_ms": float,
    "results": list[dict],
    "metadata": dict  # handler-specific, but always present
}
```

这意味着消费 `/infer` 端点的客户端，无论后端是 YOLOv8、DETR 还是 OWL-ViT，都会收到相同的外层信封结构。

## 缓存与并发交互

生命周期不仅是功能性的，也是运维性的。一条请求路径可能触发：

- **缓存命中**，并立即复用温热的模型
- **首次使用时的惰性模型加载**，第一个请求者承担完整的冷启动延迟
- **在并发限制后等待**，当运行时已经饱和时

这些交互是用户可见行为的一部分，因为它们塑造了延迟、预热成本和资源压力。

### 冷启动与热启动延迟

| 场景 | 行为 | 典型延迟影响 |
|----------|----------|----------------------|
| Cache hit | 模型已加载，立即推理 | 基线（取决于设备） |
| Lazy load | 首次请求时下载 + 初始化 | HF 模型 +2-10 秒，YOLO .pt +0.5-2 秒 |
| Memory pressure eviction | LRU 驱逐 + 重新加载 | 与惰性加载相同 |

## 故障表面

常见故障集中在四个点：

- **无效或超大输入**：在校验层捕获（Pydantic + OpenCV 检查）
- **未知模型标识符**：在注册表解析时捕获（`ModelCategory.infer_from_id()` 抛出 `ValueError`）
- **运行时模型加载故障**：在 handler `_do_load()` 处捕获；包括 HuggingFace 下载的网络错误
- **handler 内部的下游推理错误**：在 `BaseHandler._infer_impl()` 处捕获；包括 CUDA OOM 和模型特定异常

当前架构的价值在于，每种故障类型都有一个自然的边界，可以在那里被清晰地暴露出来。

## 下一步阅读

- [System Overview](/en/architecture/overview)，了解分层运行时映射
- [Handler Topology](/en/architecture/handlers)，了解执行边界如何保持清晰
- [Middleware Stack](/en/architecture/middleware-stack)，了解可观测性和防护栏如何适配
- [Model Cache](/en/architecture/model-cache)，深入了解缓存策略
