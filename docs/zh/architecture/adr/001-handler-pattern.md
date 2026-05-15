---
title: ADR-001 - Handler 模式优于工厂模式
---

# ADR-001：Handler 模式优于工厂模式

| 状态 | 日期 | 决策者 |
|------|------|--------|
| 已采纳 | 2024-01-15 | 架构团队 |

## 背景

YOLO-Toys 需要支持推理流程差异巨大的多种模型族：

- **YOLO 模型**：通过 `ultralytics.YOLO()` 加载，返回 `Results` 对象
- **HuggingFace 模型**：通过 `AutoModel.from_pretrained()` 加载，需要前后处理器
- **多模态模型**：需要额外输入如文本查询或问题

每种模型族具有独特的：
- 加载机制
- 预处理需求
- 输出格式
- 配置参数

我们需要一个能够：
1. 向调用者提供统一接口
2. 封装族特定逻辑
3. 支持轻松扩展新模型
4. 保持可测试性

的架构。

## 决策

我们采用 **策略模式（Handler 模式）**：
- `BaseHandler` 定义抽象接口
- 每个模型族有具体的 Handler 实现
- `LoadedModel` 封装加载的模型，提供简单的 `infer()` 接口
- `HandlerRegistry` 将模型 ID 解析到适当的 Handler

```python
# 策略模式方案
class BaseHandler(ABC):
    @abstractmethod
    def _do_load(self, model_id: str) -> tuple[Any, Any | None]: ...

    @abstractmethod
    def _infer_impl(self, model, processor, image, params) -> dict: ...

# 具体策略
class YOLOHandler(BaseHandler): ...
class DETRHandler(BaseHandler): ...
class BLIPCaptionHandler(BaseHandler): ...
```

## 考虑的替代方案

### 替代方案 1：工厂模式

创建生产推理函数的工厂：

```python
class InferenceFactory:
    @staticmethod
    def create(model_id: str) -> Callable:
        if model_id.endswith(".pt"):
            return YOLOInference(model_id)
        elif "detr" in model_id:
            return DETRInference(model_id)
        ...
```

**优点**：
- 简单易懂
- 无需类层次结构

**缺点**：
- 不封装状态（加载的模型、处理器）
- 难以共享公共逻辑（设备管理、错误处理）
- 返回函数而非具有丰富接口的对象

### 替代方案 2：Switch/Case 分发

中央分发的 if/elif 链：

```python
def infer(model_id: str, image, **params):
    if model_id.endswith(".pt"):
        model = load_yolo(model_id)
        return yolo_infer(model, image, params)
    elif "detr" in model_id:
        model, processor = load_detr(model_id)
        return detr_infer(model, processor, image, params)
    ...
```

**优点**：
- 简单，无抽象开销
- 易于在一处查看所有路径

**缺点**：
- 单文件无限增长
- 每个模型族无封装
- 难以单独测试各族
- 违反开闭原则

## 后果

### 正面

1. **清晰分离**：每个 Handler 拥有其模型族的逻辑
2. **可扩展性**：添加新模型需要一个新 Handler 类
3. **可测试性**：每个 Handler 可独立进行单元测试
4. **单一职责**：Handler 只知道自己的模型族
5. **开闭原则**：对扩展开放，对修改关闭

### 负面

1. **间接性**：API 调用和推理之间有多个层
2. **学习曲线**：开发者必须理解该模式
3. **样板代码**：新 Handler 需要实现抽象方法

### 缓解措施

- **间接性**：清晰的命名和本文档
- **学习曲线**：本 ADR 和学院文章
- **样板代码**：基类中的公共逻辑（`_model_to_device`、`bgr_to_pil`）

## 参考文献

- [策略模式 - GoF](https://en.wikipedia.org/wiki/Strategy_pattern)
- [深度模块原则 - Sandi Metz](https://www.sandimetz.com/blog/2016/1/20/design-mendacity-deep-module)
- [开闭原则](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)
