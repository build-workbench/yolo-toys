---
title: 深度模块设计哲学
---

# 深度模块设计哲学

YOLO-Toys 最重要的架构决策之一是使用"深度模块"——在简洁门面背后隐藏大量复杂性的接口。这种模式源自[整洁架构](/zh/citations)原则，是实现系统可维护性的关键。

## 深度模块原则

> "最好的模块是那些接口比实现简单得多的模块。"

当一个模块满足以下条件时，它就是"深度"的：
- **接口**：简单、聚焦、易于理解
- **实现**：复杂、处理多种关注点

```
┌─────────────────────────────────────────────────────────────┐
│                      深度模块                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    简洁接口                            │  │
│  │         load(model_id) → LoadedModel                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  复杂实现                              │  │
│  │  • 安全验证                                            │  │
│  │  • 注册表查找                                          │  │
│  │  • 缓存命中/未命中处理                                 │  │
│  │  • 内存压力管理                                        │  │
│  │  • CUDA 缓存清理                                       │  │
│  │  • 线程安全访问                                        │  │
│  │  • 处理器实例化                                        │  │
│  │  • 模型预热                                            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## YOLO-Toys 中的主要示例

### `LoadedModel` 包装器

`LoadedModel` 类是典型的深度模块：

```python
class LoadedModel:
    """已加载的模型及其处理器和元数据。"""
    model: Any
    processor: Any | None
    handler: BaseHandler
    loaded_at: datetime

    # 调用者看到的是：
    def infer(self, image: bytes, params: InferenceParams) -> dict:
        """在已加载的模型上执行推理。"""
        # 内部处理：
        # - 图像预处理（处理器特定）
        # - 参数编组（模型特定）
        # - 输出标准化
        # - 错误处理
        # - 计时指标
```

**调用者看到的**：一个简单的 `infer(image, params)` 方法。

**它隐藏的内容**：
- 处理器分发逻辑
- 图像预处理流水线
- 模型特定参数提取
- 输出格式标准化
- 性能计时
- 错误恢复

### `InferenceParams` 数据类

```python
@dataclass
class InferenceParams:
    """具有模型特定提取功能的推理参数。"""
    conf: float = 0.25
    iou: float = 0.45
    max_det: int = 300
    device: str = "auto"
    imgsz: int = 640
    half: bool = False
    text_queries: str | None = None
    question: str | None = None

    def for_yolo(self) -> dict:
        """提取 YOLO 特定参数。"""
        return {
            "conf": self.conf,
            "iou": self.iou,
            "max_det": self.max_det,
            "device": self.device,
            "imgsz": self.imgsz,
            "half": self.half,
        }

    def for_detr(self) -> dict:
        """提取 DETR 特定参数。"""
        return {
            "device": self.device,
            # DETR 不使用 conf、iou 等
        }
```

**调用者看到的**：一个具有合理默认值的数据类。

**它隐藏的内容**：
- 参数验证逻辑
- 模型特定参数子集
- 默认值管理
- 类型转换

### `ModelManager` 控制平面

```python
class ModelManager:
    """运行时的控制平面。"""

    def infer(self, model_id: str, image: bytes, **kwargs) -> dict:
        """所有推理的单入口点。"""
        # 调用者看到：一个方法
        # 内部：安全检查、缓存查找、处理器分发、
        #       内存管理、指标收集、错误处理
```

**调用者看到的**：`infer(model_id, image, **kwargs)`

**它隐藏的内容**：
- 安全验证（路径遍历、魔术数字）
- 缓存命中/未命中决策树
- 内存压力下的 LRU 驱逐
- 处理器注册表查找
- 线程安全的模型加载
- Prometheus 指标记录

## 为什么深度模块很重要

### 1. 降低认知负担

浅模块要求调用者理解实现细节：

```python
# 没有深度模块（浅模块）
model = registry.lookup(model_id)
handler = handler_factory.create(model.category)
params = handler.extract_params(kwargs)
image = handler.preprocess(image)
result = handler.infer(model, image, params)
output = handler.postprocess(result)
```

```python
# 使用深度模块
result = manager.infer(model_id, image, **kwargs)
```

### 2. 变更隔离

当实现变更时，调用者无需更新：

```python
# 添加新模型族只需要：
# 1. 新的处理器类
# 2. 注册表条目
# 所有现有调用者继续工作
```

### 3. 测试简化

深度模块有清晰的边界用于模拟：

```python
# 测试只需模拟简单接口
def test_detection(monkeypatch):
    def fake_infer(model_id, image, **kwargs):
        return {"detections": [...]}
    monkeypatch.setattr(manager, "infer", fake_infer)
```

## 反模式：浅模块

浅模块暴露实现细节：

```python
# 反模式：一切都是公开的
class ModelManagerShallow:
    def __init__(self):
        self.cache = ModelCache()      # 暴露！
        self.registry = HandlerRegistry()  # 暴露！
        self.handlers = {}             # 暴露！

    # 调用者必须理解所有这些
    def get_cache_stats(self): ...
    def register_handler(self, category, handler): ...
    def load_model_direct(self, model_id): ...
    def check_memory(self): ...
    def clear_cuda_cache(self): ...
```

这会导致：
- **耦合**：调用者依赖内部结构
- **脆弱性**：变更会破坏调用者
- **复杂性**：每个人都必须理解一切

## 接口成本原则

每个公共接口都有成本：

- **文档成本**：每个公共方法都需要文档
- **测试成本**：每个公共方法都需要测试
- **维护成本**：每个公共方法都是一个约束
- **学习成本**：每个公共方法都必须被学习

深度模块在最大化功能的同时最小化接口面积。

## 实践指南

### 1. 从接口开始

先写调用点：

```python
# 我想写什么？
result = manager.infer("yolov8n.pt", image, conf=0.5)
```

然后实现使该接口成为可能。

### 2. 隐藏基础设施

调用者不应该知道：
- 缓存实现
- 线程细节
- 资源管理
- 日志机制

### 3. 为复杂子系统提供门面

如果一个子系统有 10 个类，创建一个门面：

```python
# 不暴露 10 个类
model_cache = ModelCache(...)
handler_registry = HandlerRegistry(...)
security_validator = SecurityValidator(...)
# ... 还有 7 个

# 暴露一个门面
manager = ModelManager(...)  # 内部使用以上所有
```

### 4. 使用参数对象而非多个参数

```python
# 浅模块：8 个参数
def infer(model_id, image, conf, iou, max_det, device, imgsz, half):
    ...

# 深模块：1 个带默认值的参数对象
def infer(model_id, image, params=None):
    params = params or InferenceParams()
    ...
```

## 参考文献

<CitationBlock :number="1" authors="Martin, Robert C." title="Clean Architecture: A Craftsman's Guide to Software Structure and Design" venue="Prentice Hall" year="2017" />

<CitationBlock :number="2" authors="Parnas, David L." title="On the Criteria to Be Used in Decomposing Systems into Modules" venue="Communications of the ACM" year="1972" />

## 推荐阅读

<CrossReference href="/zh/academy/handler-pattern" section="学院" label="Handler 模式" />
<CrossReference href="/zh/architecture/overview" section="架构" label="系统总览" />
