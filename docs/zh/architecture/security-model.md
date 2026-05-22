---
title: 安全模型
---

# 安全模型

YOLO-Toys 实施纵深防御安全原则。每一层独立保证一个安全属性，确保信任边界中不存在单点故障。

<SvgRenderer src="/images/security-boundary.svg" alt="安全边界图" />

## 防御层

### 第一层：传输安全

所有响应都包含安全头：

```python
class SecurityHeadersMiddleware:
    async def __call__(self, scope, receive, send):
        # 为所有响应添加安全头
        headers = [
            (b"x-content-type-options", b"nosniff"),
            (b"x-frame-options", b"DENY"),
            (b"x-xss-protection", b"1; mode=block"),
            (b"referrer-policy", b"strict-origin-when-cross-origin"),
            (b"permissions-policy", b"accelerometer=(), camera=(), geolocation=()"),
        ]
```

| 头部 | 目的 |
|------|------|
| `X-Content-Type-Options: nosniff` | 防止 MIME 嗅探 |
| `X-Frame-Options: DENY` | 阻止点击劫持 |
| `X-XSS-Protection` | 遗留 XSS 过滤器（纵深防御） |
| `Referrer-Policy` | 限制 referrer 信息 |
| `Permissions-Policy` | 限制浏览器功能 |

### 第二层：流量控制

**速率限制**

```python
class RateLimitMiddleware:
    def __init__(self, app, requests_per_minute: int = 60):
        self.app = app
        self.buckets: dict[str, TokenBucket] = {}
        self.rpm = requests_per_minute
```

每 IP 令牌桶具有：
- 可配置速率（默认：60 请求/分钟）
- 自动清理过期桶
- 带有 `Retry-After` 头的优雅 429 响应

**超时保护**

```python
class TimeoutMiddleware:
    async def __call__(self, scope, receive, send):
        try:
            await asyncio.wait_for(
                self.app(scope, receive, send),
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            # 返回 504 Gateway Timeout
```

### 第三层：代理兼容性

**CORS 配置**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

**GZip 压缩**

```python
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 第四层：输入验证

**路径遍历防护**

```python
def validate_model_id(model_id: str) -> str:
    # 先进行 URL 解码（捕获编码攻击）
    decoded = urllib.parse.unquote(model_id)

    forbidden = ["../", "..\\", "/", "\\", "\x00"]
    for pattern in forbidden:
        if pattern in model_id or pattern in decoded:
            raise SecurityError(f"禁止的模式：{pattern}")

    return model_id
```

这可以捕获：
- 直接遍历：`../../../etc/passwd`
- URL 编码：`%2e%2e%2f%2e%2e%2f`
- 混合编码：`..%2f..%2f`
- 空字节：`model.pt%00.exe`

**魔术数字验证**

```python
def validate_image(data: bytes) -> None:
    # 检查文件签名（魔术数字）
    signatures = {
        b'\xff\xd8\xff': 'JPEG',
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'GIF87a': 'GIF',
        b'GIF89a': 'GIF',
        b'RIFF': 'WebP',
    }

    for sig, fmt in signatures.items():
        if data.startswith(sig):
            return

    raise SecurityError("无效的图像格式")
```

**文件大小限制**

```python
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
```

### 第五层：执行隔离

每个处理器验证自己的参数：

```python
class InferenceParams:
    conf: float = 0.25  # 范围：0.0-1.0
    iou: float = 0.45   # 范围：0.0-1.0
    max_det: int = 300  # 范围：1-1000

    def __post_init__(self):
        if not 0 <= self.conf <= 1:
            raise ValueError("conf 必须在 [0, 1] 范围内")
        if not 0 <= self.iou <= 1:
            raise ValueError("iou 必须在 [0, 1] 范围内")
        if not 1 <= self.max_det <= 1000:
            raise ValueError("max_det 必须在 [1, 1000] 范围内")
```

## 内存安全

缓存通过以下方式防止 OOM：

1. **最大大小限制** —— 缓存模型的硬上限
2. **内存阈值** —— 85% 使用时主动驱逐
3. **CUDA 缓存清理** —— GPU 内存回收

```python
def __setitem__(self, key: str, value: LoadedModel) -> None:
    with self._lock:
        if get_memory_usage() > self._memory_threshold:
            self._evict_lru_unsafe()
            torch.cuda.empty_cache()
        super().__setitem__(key, value)
```

## 审计追踪

所有安全相关事件都会被记录：

```python
logger.warning(
    "安全：路径遍历尝试",
    extra={
        "model_id": model_id,
        "client_ip": client_ip,
        "user_agent": user_agent,
    }
)
```

## 配置参考

| 变量 | 默认值 | 安全影响 |
|------|--------|---------|
| `MAX_UPLOAD_MB` | `10` | 限制通过大文件上传进行 DoS |
| `MAX_CONCURRENCY` | `4` | 限制资源耗尽 |
| `MODEL_CACHE_MAXSIZE` | `10` | 限制内存使用 |
| `MODEL_MEMORY_THRESHOLD` | `0.85` | 触发主动清理 |
| `CORS_ORIGINS` | `[]` | 限制跨域访问 |

## 威胁模型

| 威胁 | 缓解措施 |
|------|---------|
| 路径遍历 | 第四层验证 |
| DoS（上传大小） | 文件大小限制 |
| DoS（请求速率） | 速率限制 |
| DoS（内存） | 缓存驱逐 + 内存阈值 |
| 点击劫持 | X-Frame-Options |
| MIME 嗅探 | X-Content-Type-Options |
| 信息泄露 | Referrer-Policy |
| 参数注入 | 类型验证 + 范围检查 |

## 推荐阅读

<CrossReference href="/zh/architecture/middleware-stack" section="架构" label="中间件栈" />
<CrossReference href="/zh/api/error-codes" section="API" label="错误码" />
