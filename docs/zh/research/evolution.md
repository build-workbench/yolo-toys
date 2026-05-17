# 架构演进

本章追溯了 YOLO-Toys 是如何形成其当前设计的。它不是变更日志；而是关于架构决策、走过的死胡同，以及使当前边界成为必要的推理过程的叙述。

## 从扁平端点到 Handler 边界

运行时的最早版本为每个模型族暴露一个 FastAPI 端点：

```python
@app.post("/yolo/infer")
async def yolo_infer(...): ...

@app.post("/detr/infer")
async def detr_infer(...): ...
```

这对两个模型族有效。但对五个模型族就不行了。每个新模型族都重复了：

- 参数验证
- 图像预处理
- 模型加载逻辑
- 结果格式化
- 错误处理

这种重复不仅仅是代码；它是**概念上的**。每个端点都重新实现了相同的"加载模型、运行推理、返回 JSON"的契约。

### 提取

第一个架构动作是提取一个带有两个抽象方法的 `BaseHandler`：

```python
class BaseHandler(ABC):
    def _do_load(self, model_id: str) -> tuple[Any, Any | None]: ...
    def _infer_impl(self, model, processor, image, params) -> dict: ...
```

这是应用于模型推理的**模板方法模式**。`ModelManager` 调用 `handler.load()` 和 `loaded.infer()`，而无需知道底层是哪个模型族。每个 Handler 子类拥有其模型族的特性：YOLO 使用 `ultralytics.YOLO`，DETR 使用 `transformers.DetrForObjectDetection`，BLIP 使用 `BlipProcessor` 和 `BlipForConditionalGeneration`。

### 边界的代价

Handler 边界并非没有代价。它增加了：

- 每次推理调用增加一层间接
- 需要一个注册表来将模型 ID 映射到 Handler 类
- 需要约束，将模型族特定的代码保留在 Handler 内部

这种权衡是值得的，因为替代方案——将模型族逻辑分散在路由处理器中——在代码量和认知负担上都难以扩展。

## 从硬编码分发到注册表推断

第二次演进是分发机制。最初，管理器使用硬编码的 `if/elif` 链：

```python
if "yolo" in model_id:
    handler = YOLOHandler(device)
elif "detr" in model_id:
    handler = DETRHandler(device)
```

这很脆弱。添加一个新模型族意味着要修改 `ModelManager`。解决方案是将分发移入一个带有**类别推断**的注册表：

```python
class ModelCategory(Enum):
    YOLO_DETECT = auto()
    HF_DETR = auto()
    HF_OWLVIT = auto()
    # ...

    @classmethod
    def infer_from_id(cls, model_id: str) -> "ModelCategory": ...
```

`HandlerRegistry` 将类别映射到 Handler 类。管理器向注册表请求一个 Handler，注册表从模型 ID 推断出类别。

### 自修复推断

推断链被设计为对常见约定具有**自修复**能力：

1. 已知模型的精确注册表查找
2. `.pt` 扩展名 → YOLO 族
3. 关键词匹配（`detr`、`owlvit`、`blip` 等）
4. HuggingFace 路径（`/`）→ DETR 回退

这意味着添加一个新的 YOLOv8 权重文件不需要注册表条目。但添加一个全新的模型族（例如 RT-DETR）确实需要扩展 `ModelCategory` 和 `_CATEGORY_HANDLER_MAP`。

## 从朴素缓存到运营感知

第一个缓存是一个普通的字典：

```python
self._cache: dict[str, Any] = {}
```

它无限期地持有模型。它不是线程安全的。它没有淘汰策略。在显存有限的 GPU 上，这会导致 OOM 崩溃。

当前的 `ModelCache` 是**第三代**设计：

| Generation | Eviction | Thread safety | Memory awareness |
|-----------|-----------|---------------|----------------|
| v1: dict | None | No | No |
| v2: TTLCache | TTL only | No | No |
| v3: ModelCache | LRU + TTL | Yes | Yes |

LRU + TTL 混合缓存是生产级视觉服务运行时的最小可行缓存。它不是分布式缓存，不是持久化缓存，也不做模型量化。但它解决了正确的问题：**保持热模型温热而不耗尽主机内存**。

## OpenSpec 层

最新的架构补充是 OpenSpec 系统：一组规范和变更工件，在编写代码之前记录运行时的行为。

对于这样规模的项目来说，这很不寻常。大多数这样小的代码库依赖 README + 代码。YOLO-Toys 增加了 OpenSpec，因为目标受众——面试官、评审者、贡献者——需要**可追溯的设计原理**，而不仅仅是能工作的代码。

OpenSpec 工作流：

1. **探索**（`/opsx:explore`）——调查问题或想法
2. **提议**（`/opsx:propose`）——编写包含设计、任务和验收标准的规范
3. **应用**（`/opsx:apply`）——按照规范实现
4. **评审**（`/review`）——在阶段边界进行验证
5. **归档**（`/opsx:archive`）——清理已完成的变更

这个工作流使代码库保持**文档化状态**，而非临时状态。

## 未来方向

架构并未冻结。以下是正在研究的活跃领域：

| Direction | Status | Open questions |
|-----------|--------|---------------|
| Batch inference | Proposed | 如何在批处理异构模型族的同时不丢失每请求的语义 |
| Model quantization | Research | 每个模型族的 INT8/FP16 量化权衡；内存 vs 精度 |
| Streaming protocol v2 | Design | 用于降低 WebSocket 开销的二进制帧编码（MessagePack 或 protobuf） |
| Multi-GPU sharding | Future | 如何在多个 CUDA 设备间分布模型缓存 |
| gRPC surface | Future | gRPC 是否带来足够的延迟收益以证明其复杂性 |

## 接下来阅读

- [参考文献](/en/citations)，了解影响这些决策的论文和项目
- [Handler 模式](/en/academy/handler-pattern)，了解设计模式的深入解析
- [缓存策略](/en/academy/caching-strategy)，了解缓存设计原理
