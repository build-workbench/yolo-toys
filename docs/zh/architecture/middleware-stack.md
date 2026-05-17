# 中间件栈

YOLO-Toys 运行时提供了一个分层的中间件栈，它将一个简单的 FastAPI 应用转变为可用于生产环境的服务。每一层只负责单一、定义明确的关注点，并且它们的排列顺序确保了运维可见性和安全性在业务逻辑运行之前生效。

## 栈的排列顺序

```
┌─────────────────────────────────────────────────────────────┐
│  Client Request                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  SecurityHeadersMiddleware                                  │
│  → Adds security-related HTTP response headers              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  MetricsMiddleware                                          │
│  → Records Prometheus histograms + periodic memory sampling  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  TimeoutMiddleware                                          │
│  → Warns when request duration exceeds threshold            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  RateLimitMiddleware                                        │
│  → Per-IP token-bucket rate limiting in memory              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  GZipMiddleware                                             │
│  → Compresses responses above minimum size                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  CORSMiddleware                                             │
│  → Cross-origin access control with origin allow-list       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Application (FastAPI routes)                               │
└─────────────────────────────────────────────────────────────┘
```

## 为什么这个顺序很重要

FastAPI 按照**反向注册顺序**应用中间件：最后注册的中间件是最外层的包装器。YOLO-Toys 的注册顺序如下：

```python
app.add_middleware(SecurityHeadersMiddleware)      # outermost
app.add_middleware(MetricsMiddleware)
app.add_middleware(TimeoutMiddleware, timeout_seconds=60.0)
app.add_middleware(RateLimitMiddleware, requests_per_minute=...)
app.add_middleware(GZipMiddleware, minimum_size=...)
app.add_middleware(CORSMiddleware, ...)              # innermost, closest to app
```

这意味着实际的执行顺序是：**CORS → GZip → RateLimit → Timeout → Metrics → SecurityHeaders**。

理由如下：
- **CORS 在前**，这样预检 `OPTIONS` 请求不会触发更重的层
- **GZip 其次**，这样压缩会在所有处理完成后、在最终响应上执行
- **RateLimit 在 Timeout 之前**，这样滥用请求会在消耗超时预算之前被拒绝
- **Metrics 在 SecurityHeaders 之前**，这样指标层能看到真实的状态码，包括错误
- **SecurityHeaders 在最外层**，这样每个响应（包括错误响应）都会带上安全响应头

## SecurityHeadersMiddleware

该中间件为每个出站响应添加一组基础的安全相关 HTTP 响应头：

| Header | Value | Purpose |
|--------|-------|---------|
| `X-Content-Type-Options` | `nosniff` | 阻止 MIME 类型嗅探 |
| `X-Frame-Options` | `DENY` | 阻止通过 iframe 嵌入的点击劫持 |
| `X-XSS-Protection` | `1; mode=block` | 启用浏览器 XSS 过滤器 |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | 限制 referrer 泄漏 |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=()` | 禁用敏感浏览器 API |

::: tip 提示
HSTS (`Strict-Transport-Security`) 被有意省略。只有在具备经验证的 HTTPS 终止能力的生产环境中，启用它才是安全的。部署指南介绍了如何通过反向代理添加它。
:::

## MetricsMiddleware

该层将 Prometheus 监控集成到每个请求中：

```python
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            status_code = 500
            raise
        finally:
            duration = time.time() - start_time
            HTTP_REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=str(status_code)
            ).observe(duration)
```

关键设计决策：
- **在 `finally` 中追踪状态码**：确保即使异常路径也会被记录（记为 500）
- **周期性内存采样**：每 10 秒，内存使用量会被推送到一个 Prometheus gauge
- **端点级粒度**：每个路由都被独立打标，以便进行细粒度的延迟分析

## RateLimitMiddleware

一个轻量的、基于内存的 token-bucket 实现：

```python
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: dict[str, list[float]] = {}
        self._lock = threading.Lock()
        self._max_ips = 10000
```

### 内存安全设计

该中间件实现了**自清理**机制，以防止无限制的内存增长：

1. **逐请求过滤**：每次请求时，该 IP 超过 60 秒的时间戳会被过滤掉
2. **周期性全面清理**：每 60 秒，过期的 IP 会被完全移除
3. **IP 上限强制执行**：如果 IP 数量超过 10,000，最老的 IP 会被驱逐

::: warning 生产环境提示
该内存中的速率限制器适用于单实例部署。对于多副本或高流量的生产环境，请将其替换为基于 Redis 的限制器。
:::

## TimeoutMiddleware

一个软超时监控器，当请求超过阈值时记录警告：

```python
class TimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        if duration > self.timeout:
            logger.warning(
                "Request to %s took %.2fs (timeout: %.2fs)",
                request.url.path, duration, self.timeout
            )
        return response
```

::: info 说明
这是一个**软超时**（仅记录日志），因为 Python 的 asyncio 不支持以模型推理安全的方式按请求取消。真正的请求取消应该在反向代理层实现（例如，NGINX 的 `proxy_read_timeout`）。
:::

## 延伸阅读

- [配置注入](/zh/architecture/config-injection)，了解中间件参数如何通过设置进行连接
- [系统总览](/zh/architecture/overview)，了解中间件在运行时拓扑中的位置
- [请求生命周期](/zh/architecture/request-flow)，追踪请求穿过所有层的端到端路径
