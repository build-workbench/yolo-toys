---
title: 模型加载流程
---

# 模型加载流程

模型加载子系统是 YOLO-Toys 运行时行为的核心。它结合了延迟加载、TTL 新鲜度和内存压力下的 LRU 驱逐，在最大化热模型复用的同时提供可预测的资源使用。

<SvgRenderer src="/images/model-loading.svg" alt="模型加载流程图" />

## 核心问题

服务多种模型族会产生一个基本的矛盾：

1. **加载模型代价高昂** —— YOLOv8x 在现代 GPU 上加载需要 2-4 秒
2. **内存有限** —— 单个 YOLOv8x 可能占用 200MB+ GPU 内存
3. **工作负载呈突发性** —— 用户不会均匀地请求模型

解决方案必须平衡：
- **延迟**：最小化冷启动惩罚
- **内存**：保持在硬件限制内
- **新鲜度**：尊重模型更新周期

## 架构概览

```
┌──────────────────────────────────────────────────────────────┐
│                      ModelManager                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐ │
│  │   安全检查      │→│   缓存查找      │→│  处理器选择   │ │
│  └─────────────────┘  └─────────────────┘  └───────────────┘ │
│                              ↓                                │
│                    ┌─────────────────┐                        │
│                    │   ModelCache    │                        │
│                    │  (TTL + LRU)    │                        │
│                    └─────────────────┘                        │
└──────────────────────────────────────────────────────────────┘
```

## 缓存策略：TTL + LRU 混合

### 为什么两者都要？

| 策略 | 保证什么 | 遗漏什么 |
|------|---------|---------|
| **仅 TTL** | 新鲜度（模型过期） | 无内存压力处理 |
| **仅 LRU** | 内存边界 | 陈旧模型永远存在 |
| **TTL + LRU** | 新鲜度和边界兼顾 | 复杂性 |

混合方法让我们兼得两者之长。

### TTL（生存时间）

```python
# 默认：3600 秒（1 小时）
MODEL_CACHE_TTL = int(os.getenv("MODEL_CACHE_TTL", "3600"))
```

当模型的 TTL 过期时：
- 模型被标记为陈旧
- 下次访问触发重新加载
- 旧模型从缓存中驱逐

### LRU（最近最少使用）

```python
# 默认：最多 10 个模型
MODEL_CACHE_MAXSIZE = int(os.getenv("MODEL_CACHE_MAXSIZE", "10"))
```

当缓存已满且请求新模型时：
- 找到最近最少访问的模型
- 驱逐它（释放 GPU 内存）
- 加载新模型

### 内存感知驱逐

```python
# 默认：系统内存的 85%
MODEL_MEMORY_THRESHOLD = float(os.getenv("MODEL_MEMORY_THRESHOLD", "0.85"))
```

即使缓存未满，如果系统内存使用超过阈值：
- 触发主动 LRU 驱逐
- 清理 CUDA 缓存以回收 GPU 内存

```python
def _evict_lru_unsafe(self) -> None:
    """驱逐最近最少使用的模型并清理 CUDA 缓存。"""
    lru_key = min(self._access_times, key=self._access_times.get)
    del self[lru_key]
    torch.cuda.empty_cache()  # 对 GPU 内存至关重要
```

## 安全边界

在任何模型加载之前，请求都要通过安全验证：

```python
# 路径遍历防护
forbidden_patterns = ["../", "..\\", "/", "\\", "\x00"]
for pattern in forbidden_patterns:
    if pattern in model_id or pattern in decoded_id:
        raise ValueError("无效的模型 ID：禁止的模式")
```

这可以防止：
- 目录遍历攻击（`../../../etc/passwd`）
- URL 编码绕过（`%2e%2e%2f`）
- 空字节注入（`model.pt%00.exe`）

## 处理器选择

注册表将模型类别映射到处理器：

```python
class ModelCategory(Enum):
    YOLO_DETECT = auto()
    YOLO_SEGMENT = auto()
    YOLO_POSE = auto()
    HF_DETR = auto()
    HF_OWLVIT = auto()
    HF_GROUNDING_DINO = auto()
    MULTIMODAL_CAPTION = auto()
    MULTIMODAL_VQA = auto()
```

类别解析遵循优先级链：

1. **精确注册表匹配** — `MODEL_REGISTRY.get(model_id)`
2. **文件扩展名启发式** — `.pt` → YOLO
3. **HuggingFace 路径推断** — `detr`、`owlvit`、`grounding`、`blip` 关键字
4. **回退** — 任何包含 `/` 的路径 → DETR（HuggingFace）

## 线程安全

模型加载受可重入锁保护：

```python
self._lock = threading.RLock()

def get_model(self, model_id: str) -> LoadedModel:
    with self._lock:
        # 线程安全的缓存访问
        if model_id in self._cache:
            return self._cache[model_id]
        # 加载并缓存
        model = self._load_model(model_id)
        self._cache[model_id] = model
        return model
```

这确保：
- 多个请求命中冷缓存时不会出现竞态条件
- 原子性的检查-然后-加载操作
- 来自异步处理器的安全并发访问

## 配置参考

| 环境变量 | 默认值 | 描述 |
|---------|--------|------|
| `MODEL_CACHE_MAXSIZE` | `10` | 最大缓存模型数 |
| `MODEL_CACHE_TTL` | `3600` | 缓存 TTL（秒） |
| `MODEL_MEMORY_THRESHOLD` | `0.85` | 内存阈值（0-1） |
| `MAX_CONCURRENCY` | `4` | 最大并发推理数 |
| `SKIP_WARMUP` | `false` | 启动时跳过模型预热 |

## 推荐阅读

<CrossReference href="/zh/architecture/handlers" section="架构" label="处理器体系" />
<CrossReference href="/zh/academy/caching-strategy" section="学院" label="缓存策略深入" />
