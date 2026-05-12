# 添加自定义模型

逐步指南：使用你自己的模型扩展 YOLO-Toys。

---

## 📋 前提条件

- Python 3.11+ 已安装
- YOLO-Toys 开发环境已配置
- 了解你想添加的模型

---

## 🚀 快速开始

添加模型需要 3 个步骤：

1. **创建 Handler** — 实现 `load()` 和 `infer()` 方法
2. **注册模型** — 添加带元数据的注册表
3. **添加测试** — 验证实现

---

## 📝 步骤 1：创建 Handler

在 `app/handlers/` 中创建新文件：

```python
# app/handlers/my_model_handler.py
from app.handlers.base import BaseHandler

class MyModelHandler(BaseHandler):
    def load(self, model_id: str) -> tuple:
        # 加载模型和处理器
        model = load_my_model(model_id)
        return model, processor

    def infer(self, model, processor, image, **params) -> dict:
        # 运行推理
        result = model(image)
        return self.make_result(image, detections, "detect", ...)
```

---

## 🔌 步骤 2：注册模型

编辑 `app/handlers/registry.py`：

```python
from app.handlers.my_model_handler import MyModelHandler

# 添加类别
class ModelCategory(Enum):
    MY_MODEL = "my_model"

# 注册 Handler
_CATEGORY_HANDLER_MAP = {
    ModelCategory.MY_MODEL: MyModelHandler,
}

# 添加模型元数据
MODEL_REGISTRY["my-model-v1"] = {
    "category": ModelCategory.MY_MODEL,
    "name": "My Model v1",
    "task": "detect",
}
```

---

## 🧪 步骤 3：添加测试

```python
# tests/test_my_model.py
def test_my_model_handler():
    handler = MyModelHandler(device="cpu")
    model, processor = handler.load("my-model-v1")
    result = handler.infer(model, processor, test_image, conf=0.5)
    assert "detections" in result
```

---

## 🔗 相关文档

- [Handler 模式](../architecture/handlers) — Handler 实现详情
- [架构](../architecture/overview) — 系统架构
