---
title: Security Model
---

# Security Model

YOLO-Toys implements defense-in-depth security principles. Each layer independently guarantees a security property, ensuring no single point of failure in the trust boundary.

<SvgRenderer src="/images/security-boundary.svg" alt="Security boundary diagram" />

## Defense Layers

### Layer 1: Transport Security

All responses include security headers:

```python
class SecurityHeadersMiddleware:
    async def __call__(self, scope, receive, send):
        # Add security headers to all responses
        headers = [
            (b"x-content-type-options", b"nosniff"),
            (b"x-frame-options", b"DENY"),
            (b"x-xss-protection", b"1; mode=block"),
            (b"referrer-policy", b"strict-origin-when-cross-origin"),
            (b"permissions-policy", b"accelerometer=(), camera=(), geolocation=()"),
        ]
```

| Header | Purpose |
|--------|---------|
| `X-Content-Type-Options: nosniff` | Prevents MIME sniffing |
| `X-Frame-Options: DENY` | Blocks clickjacking |
| `X-XSS-Protection` | Legacy XSS filter (defense in depth) |
| `Referrer-Policy` | Limits referrer information |
| `Permissions-Policy` | Restricts browser features |

### Layer 2: Traffic Control

**Rate Limiting**

```python
class RateLimitMiddleware:
    def __init__(self, app, requests_per_minute: int = 60):
        self.app = app
        self.buckets: dict[str, TokenBucket] = {}
        self.rpm = requests_per_minute
```

Per-IP token bucket with:
- Configurable rate (default: 60 requests/minute)
- Auto-cleanup of stale buckets
- Graceful 429 responses with `Retry-After` header

**Timeout Protection**

```python
class TimeoutMiddleware:
    async def __call__(self, scope, receive, send):
        try:
            await asyncio.wait_for(
                self.app(scope, receive, send),
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            # Return 504 Gateway Timeout
```

### Layer 3: Proxy Compatibility

**CORS Configuration**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

**GZip Compression**

```python
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Layer 4: Input Validation

**Path Traversal Protection**

```python
def validate_model_id(model_id: str) -> str:
    # URL decode first (catch encoded attacks)
    decoded = urllib.parse.unquote(model_id)

    forbidden = ["../", "..\\", "/", "\\", "\x00"]
    for pattern in forbidden:
        if pattern in model_id or pattern in decoded:
            raise SecurityError(f"Forbidden pattern: {pattern}")

    return model_id
```

This catches:
- Direct traversal: `../../../etc/passwd`
- URL-encoded: `%2e%2e%2f%2e%2e%2f`
- Mixed encoding: `..%2f..%2f`
- Null byte: `model.pt%00.exe`

**Magic Number Validation**

```python
def validate_image(data: bytes) -> None:
    # Check file signature (magic numbers)
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

    raise SecurityError("Invalid image format")
```

**File Size Limits**

```python
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
```

### Layer 5: Execution Isolation

Each handler validates its own parameters:

```python
class InferenceParams:
    conf: float = 0.25  # Range: 0.0-1.0
    iou: float = 0.45   # Range: 0.0-1.0
    max_det: int = 300  # Range: 1-1000

    def __post_init__(self):
        if not 0 <= self.conf <= 1:
            raise ValueError("conf must be in [0, 1]")
        if not 0 <= self.iou <= 1:
            raise ValueError("iou must be in [0, 1]")
        if not 1 <= self.max_det <= 1000:
            raise ValueError("max_det must be in [1, 1000]")
```

## Memory Safety

The cache prevents OOM through:

1. **Max size limit** — Hard cap on cached models
2. **Memory threshold** — Proactive eviction at 85% usage
3. **CUDA cache clearing** — GPU memory reclamation

```python
def __setitem__(self, key: str, value: LoadedModel) -> None:
    with self._lock:
        if get_memory_usage() > self._memory_threshold:
            self._evict_lru_unsafe()
            torch.cuda.empty_cache()
        super().__setitem__(key, value)
```

## Audit Trail

All security-relevant events are logged:

```python
logger.warning(
    "Security: path traversal attempt",
    extra={
        "model_id": model_id,
        "client_ip": client_ip,
        "user_agent": user_agent,
    }
)
```

## Configuration Reference

| Variable | Default | Security Impact |
|----------|---------|-----------------|
| `MAX_UPLOAD_MB` | `10` | Limits DoS via large uploads |
| `MAX_CONCURRENCY` | `4` | Limits resource exhaustion |
| `MODEL_CACHE_MAXSIZE` | `10` | Limits memory usage |
| `MODEL_MEMORY_THRESHOLD` | `0.85` | Triggers proactive cleanup |
| `CORS_ORIGINS` | `[]` | Restricts cross-origin access |

## Threat Model

| Threat | Mitigation |
|--------|------------|
| Path traversal | Layer 4 validation |
| DoS (upload size) | File size limits |
| DoS (request rate) | Rate limiting |
| DoS (memory) | Cache eviction + memory threshold |
| Clickjacking | X-Frame-Options |
| MIME sniffing | X-Content-Type-Options |
| Info disclosure | Referrer-Policy |
| Parameter injection | Type validation + range checks |

## What to Read Next

<CrossReference href="/en/architecture/middleware-stack" section="Architecture" label="Middleware Stack" />
<CrossReference href="/en/api/error-codes" section="API" label="Error Codes" />
