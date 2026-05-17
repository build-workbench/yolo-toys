# Middleware Stack

The YOLO-Toys runtime ships a layered middleware stack that turns a simple FastAPI application into a production-ready service. Each layer has a single, well-defined concern, and they are ordered so that operational visibility and safety are applied before business logic runs.

## Stack ordering

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

## Why this ordering matters

FastAPI applies middleware in **reverse registration order**: the last middleware registered is the outermost wrapper. YOLO-Toys registers them as:

```python
app.add_middleware(SecurityHeadersMiddleware)      # outermost
app.add_middleware(MetricsMiddleware)
app.add_middleware(TimeoutMiddleware, timeout_seconds=60.0)
app.add_middleware(RateLimitMiddleware, requests_per_minute=...)
app.add_middleware(GZipMiddleware, minimum_size=...)
app.add_middleware(CORSMiddleware, ...)              # innermost, closest to app
```

This means the actual execution order is: **CORS → GZip → RateLimit → Timeout → Metrics → SecurityHeaders**.

The rationale:
- **CORS first** so preflight `OPTIONS` requests do not trigger heavier layers
- **GZip next** so compression happens on the final response, after all processing
- **RateLimit before Timeout** so abusive requests are rejected before consuming timeout budget
- **Metrics before SecurityHeaders** so the metrics layer sees the true status code, including errors
- **SecurityHeaders outermost** so every response, including error responses, gets the security headers

## SecurityHeadersMiddleware

This middleware adds a baseline of security-related HTTP response headers on every outgoing response:

| Header | Value | Purpose |
|--------|-------|---------|
| `X-Content-Type-Options` | `nosniff` | Prevents MIME-type sniffing |
| `X-Frame-Options` | `DENY` | Prevents clickjacking via iframe embedding |
| `X-XSS-Protection` | `1; mode=block` | Enables browser XSS filter |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limits referrer leakage |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=()` | Disables sensitive browser APIs |

::: tip Note
HSTS (`Strict-Transport-Security`) is intentionally omitted. It is only safe to enable in production environments with verified HTTPS termination. The deployment guide covers how to add it via a reverse proxy.
:::

## MetricsMiddleware

This layer integrates Prometheus instrumentation into every request:

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

Key design decisions:
- **Status code tracking in `finally`**: ensures even exception paths are recorded (as 500)
- **Periodic memory sampling**: every 10 seconds, memory usage is pushed to a Prometheus gauge
- **Endpoint-level granularity**: each route is labeled independently for fine-grained latency analysis

## RateLimitMiddleware

A lightweight, in-memory token-bucket implementation:

```python
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: dict[str, list[float]] = {}
        self._lock = threading.Lock()
        self._max_ips = 10000
```

### Memory safety design

The middleware implements **self-cleaning** to prevent unbounded memory growth:

1. **Per-request filtering**: on each request, timestamps older than 60 seconds are filtered out for that IP
2. **Periodic full cleanup**: every 60 seconds, expired IPs are removed entirely
3. **IP cap enforcement**: if the IP count exceeds 10,000, the oldest IPs are evicted

::: warning Production Note
This in-memory rate limiter is suitable for single-instance deployments. For multi-replica or high-traffic production environments, replace it with a Redis-backed limiter.
:::

## TimeoutMiddleware

A soft-timeout monitor that logs warnings when requests exceed the threshold:

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

::: info Note
This is a **soft timeout** (logging only) because Python's asyncio does not support per-request cancellation in a way that is safe for model inference. True request cancellation should be implemented at the reverse-proxy layer (e.g., NGINX `proxy_read_timeout`).
:::

## What to read next

- [Config Injection](/en/architecture/config-injection) for how middleware parameters are wired through settings
- [System Overview](/en/architecture/overview) for where middleware fits in the runtime topology
- [Request Lifecycle](/en/architecture/request-flow) for the end-to-end path through all layers
