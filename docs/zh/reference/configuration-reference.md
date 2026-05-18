---
title: 配置参考
---

# 配置参考

YOLO-Toys 遵循 [十二因素应用](https://12factor.net/config) 方法论，通过环境变量进行所有配置。配置通过 Pydantic Settings 进行类型安全校验。

## 核心服务器设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `PORT` | `int` | `8000` | 服务器端口 |
| `HOST` | `str` | `0.0.0.0` | 绑定地址 |
| `LOG_LEVEL` | `str` | `INFO` | 日志级别（DEBUG、INFO、WARNING、ERROR） |
| `WORKERS` | `int` | `1` | Worker 进程数 |

```bash
export PORT=8080
export LOG_LEVEL=DEBUG
```

## 模型设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `MODEL_NAME` | `str` | `yolov8s.pt` | `/infer` 端点默认模型 |
| `DEVICE` | `str` | `auto` | 设备（auto、cpu、cuda、mps） |
| `SKIP_WARMUP` | `bool` | `false` | 启动时跳过模型预热 |

设备选择逻辑：

```
auto → 有 CUDA → 用 CUDA → 有 MPS → 用 MPS → 用 CPU
```

## 推理参数

| 变量 | 类型 | 默认值 | 范围 | 说明 |
|------|------|-------|-----|------|
| `CONF_THRESHOLD` | `float` | `0.25` | 0.0–1.0 | 置信度阈值 |
| `IOU_THRESHOLD` | `float` | `0.45` | 0.0–1.0 | NMS IoU 阈值 |
| `MAX_DET` | `int` | `300` | 1–1000 | 每图最大检测数 |
| `IMGSZ` | `int` | `640` | 32–4096 | 推理图像尺寸 |
| `HALF` | `bool` | `false` | — | FP16 推理 |

以上参数均可在单次请求中覆盖：

```json
{
  "model": "yolov8n.pt",
  "image": "<base64>",
  "conf": 0.5,
  "iou": 0.4,
  "max_det": 100
}
```

## 缓存设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `MODEL_CACHE_MAXSIZE` | `int` | `10` | 最大缓存模型数 |
| `MODEL_CACHE_TTL` | `int` | `3600` | 缓存 TTL（秒） |
| `MODEL_MEMORY_THRESHOLD` | `float` | `0.85` | 内存阈值（0–1） |

缓存行为：

```
请求 → 缓存检查
       ├─ 命中 → 返回缓存模型
       └─ 未命中 → 检查内存
                  ├─ 低于阈值 → 加载模型
                  └─ 超过阈值 → 驱逐 LRU → 加载模型
```

<div class="yt-callout yt-callout--performance">
  <div class="yt-callout__label">关键调优项</div>
  <div class="yt-callout__body">在 6 GB GPU 上运行 BLIP 或 OWL-ViT 时，建议将 <code>MODEL_CACHE_MAXSIZE</code> 设为 2–3，并保持 <code>MODEL_MEMORY_THRESHOLD=0.85</code>。参见<a href="/zh/reference/benchmarks">性能基准</a>中的安全配置表。</div>
</div>

## 并发设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `MAX_CONCURRENCY` | `int` | `4` | 最大并发推理数 |
| `REQUEST_TIMEOUT` | `int` | `60` | 请求超时（秒） |

内部通过信号量控制：

```python
self._semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

async def infer_with_limit(...):
    async with self._semaphore:
        return await self._infer_internal(...)
```

## 上传限制

| 变量 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `MAX_UPLOAD_MB` | `int` | `10` | 最大上传文件大小（MB） |

## 安全设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `RATE_LIMIT_RPM` | `int` | `60` | 每 IP 每分钟请求数限制 |
| `CORS_ORIGINS` | `str` | `""` | 逗号分隔的 CORS 来源列表 |

```bash
# 单来源
export CORS_ORIGINS="https://example.com"

# 多来源
export CORS_ORIGINS="https://example.com,https://api.example.com"

# 允许所有（仅限开发环境）
export CORS_ORIGINS="*"
```

## BLIP 专用设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `BLIP_MAX_TOKENS` | `int` | `20` | 描述生成最大 token 数 |
| `BLIP_VQA_MAX_TOKENS` | `int` | `50` | VQA 最大 token 数 |

## 监控设置

| 变量 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `METRICS_ENABLED` | `bool` | `true` | 启用 Prometheus 指标 |
| `METRICS_PORT` | `int` | `9090` | 指标服务端口 |

| 端点 | 用途 |
|------|------|
| `/metrics` | Prometheus 指标 |
| `/health` | 健康检查 + 系统信息 |
| `/system/stats` | 详细系统统计 |
| `/system/cache/clear` | 清除模型缓存（POST） |

## .env 文件示例

```env
# 服务器
PORT=8000
LOG_LEVEL=INFO

# 模型
MODEL_NAME=yolov8s.pt
DEVICE=auto

# 推理
CONF_THRESHOLD=0.25
IOU_THRESHOLD=0.45
MAX_DET=300

# 缓存
MODEL_CACHE_MAXSIZE=10
MODEL_CACHE_TTL=3600
MODEL_MEMORY_THRESHOLD=0.85

# 并发
MAX_CONCURRENCY=4
REQUEST_TIMEOUT=60

# 上传
MAX_UPLOAD_MB=10

# 安全
RATE_LIMIT_RPM=60
CORS_ORIGINS=https://example.com

# 监控
METRICS_ENABLED=true
```

## Docker 配置

```dockerfile
ENV PORT=8000
ENV DEVICE=auto
ENV MODEL_NAME=yolov8s.pt
```

```yaml
services:
  yolo-toys:
    image: yolo-toys:latest
    environment:
      - PORT=8000
      - DEVICE=cuda
      - MODEL_NAME=yolov8x.pt
      - CONF_THRESHOLD=0.3
    ports:
      - "8000:8000"
```

## 配置校验

所有设置在启动时进行校验：

```python
class AppSettings(BaseSettings):
    conf_threshold: float = 0.25

    @validator("conf_threshold")
    def validate_conf(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("conf_threshold must be in [0, 1]")
        return v
```

无效配置会以清晰的错误信息阻止启动。

## 接下来阅读什么

- [性能基准](/zh/reference/benchmarks) — 缓存配置对吞吐量的影响
- [Docker 部署](/zh/deployment/docker) — 容器环境配置实践
- [模型矩阵](/zh/reference/models) — 各模型家族资源需求
