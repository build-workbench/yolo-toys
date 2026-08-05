# 架构总览

YOLO-Toys 最易于理解的方式是将其视为一个**归一化服务运行时**。目标不是掩盖不同视觉模型行为各异的事实，而是让这些差异存在于明确的执行边界之后，而不是泄漏到每条路由、每个载荷和每个部署 concern 中。

<FigureFrame
  title="图 1. 运行时拓扑"
  caption="服务被刻意分层，使路由处理、模型解析、执行、缓存和结果整形不会坍缩到同一个抽象中。"
>
  <SvgRenderer src="/images/hero-architecture.svg" alt="YOLO-Toys runtime topology" title="Runtime Topology" />
</FigureFrame>

## 分层模型

| 层 | 职责 | 存在原因 |
| --- | --- | --- |
| API 表面 | HTTP 与 WebSocket 入口 | 将传输层 concern 与模型逻辑分离 |
| 运行时协调 | `ModelManager`、并发控制、缓存策略 | 将生命周期与资源决策集中化 |
| 分发与元数据 | `HandlerRegistry`、模型注册表条目 | 使模型查找具有确定性和可检查性 |
| 执行适配器 | YOLO、DETR、OWL-ViT、Grounding DINO、BLIP handlers | 容纳模型家族特有的行为 |
| 结果归一化 | 共享 schema 与 formatter helper | 保持一致的公共契约 |

## 核心架构押注

该项目做了一个强有力的押注：**只要将执行差异推入 handler 适配器，并对公共输出进行足够积极的归一化，异构模型就可以共享同一条服务边界**。

这一押注带来三项收益：

1. API 消费者不需要为每个模型家族采用不同的集成方式。
2. 新模型家族可以在有限的表面变动下被加入。
3. 架构权衡保持可见，因为适配器始终是明确的。

它也带来一项代价：

- 运行时必须承担更多上游模型语义与下游 API 语义之间的翻译工作。

## 为什么 manager 层是核心

`ModelManager` 不是一个便利的包装层。它是运行时的控制平面。它决定模型何时加载、缓存实例何时应被复用，以及推理请求如何在不产生路由级重复的情况下到达正确的 handler。

### 加载时的安全边界

manager 在加载任何模型之前都会强制执行路径遍历防护：

```python
# From app/model_manager.py
decoded_id = urllib.parse.unquote(model_id)
forbidden_patterns = ["../", "..\\", "/", "\\", "\x00"]
for pattern in forbidden_patterns:
    if pattern in model_id or pattern in decoded_id:
        raise ValueError("Invalid model ID: contains forbidden character sequence")
```

这是一种 deliberate 的安全姿态：模型 ID 被视为不受信任的输入，先解码，再与拒绝列表进行模式匹配，之后才到达注册表或文件系统。

### LRU + TTL 混合缓存

`ModelCache` 基于 `cachetools` 的 `TTLCache` 扩展了两项额外能力：

- **内存压力下的 LRU 驱逐**：当系统内存超过可配置阈值（默认 85%）时，最近最少使用的模型会被驱逐
- **线程安全访问**：所有缓存操作都被包裹在可重入锁中
- **CUDA 缓存清理**：当模型被驱逐时，会调用 `torch.cuda.empty_cache()` 以释放 GPU 内存

```python
class ModelCache(TTLCache[str, LoadedModel]):
    def __setitem__(self, key: str, value: Any) -> None:
        with self._lock:
            if len(self) >= self.maxsize or get_memory_usage() > self._memory_threshold:
                self._evict_lru_unsafe()
            super().__setitem__(key, value)
```

这意味着该缓存是**具有运维感知能力的**：它不仅仅按时间过期键，还会对主机资源压力做出反应。

## 为什么 registry 很重要

注册表是项目的**语义索引**。它所做的不仅仅是将 ID 映射到 handler。它还记录模型类别、任务类型、元数据和参数期望。这使服务可以通过 `/models` 进行内省，保持分发的确定性，并为文档提供单一的事实来源 backbone。

### 类别推断逻辑

`ModelCategory.infer_from_id()` 实现了一种级联解析策略：

1. **精确注册表匹配**：如果模型 ID 在 `MODEL_REGISTRY` 中，使用已注册的类别
2. **文件扩展名启发式**：`.pt` 文件被归类为 YOLO（带有 `seg`/`pose` 子变体）
3. **HuggingFace 路径推断**：`detr`、`owlvit`、`grounding`、`dino`、`blip` 关键字映射到各自的类别
4. **回退**：任何包含 `/` 的 ID 都被视为 HuggingFace DETR 模型

这一推断链意味着注册表对常见的命名约定是**自愈合的**，同时对未知输入保持严格。

## 中间件栈设计

运行时配备了一个反映生产 concern 的分层中间件栈：

```
SecurityHeaders → Metrics → Timeout → RateLimit → GZip → CORS → Application
```

| 中间件 | Concern | 关键行为 |
|------------|---------|------------|
| `SecurityHeadersMiddleware` | 响应安全 | 添加 X-Content-Type-Options、X-Frame-Options、X-XSS-Protection、Referrer-Policy、Permissions-Policy |
| `MetricsMiddleware` | 可观测性 | 通过 Prometheus 记录请求持续时间直方图；每 10 秒采样内存使用情况 |
| `TimeoutMiddleware` | 弹性 | 当请求超过可配置阈值（默认 60 秒）时发出警告 |
| `RateLimitMiddleware` | 滥用防护 | 基于内存的每 IP 令牌桶；自动清理过期条目以防止内存泄漏 |
| `GZipMiddleware` | 带宽 | 对超过大小阈值的响应进行压缩 |
| `CORSMiddleware` | 跨域 | 限制为配置的来源列表；当使用 `*` 时禁用凭证 |

在 [Middleware Stack](/zh/architecture/middleware-stack) 中阅读完整的中间件分析。

## 下一步阅读

- [Request Lifecycle](/zh/architecture/request-flow)，了解端到端推理路径
- [Handler Pattern](/zh/academy/handler-pattern)，了解适配器边界
- [Registry Pattern](/zh/academy/registry-pattern)，了解模型元数据与分发推理
- [Middleware Stack](/zh/architecture/middleware-stack)，了解运维层
- [Config Injection](/zh/architecture/config-injection)，了解设置如何流经系统
- [Model Cache](/zh/architecture/model-cache)，深入了解缓存策略
