---
title: 自定义 Handler 开发
---

# 自定义 Handler 开发

本指南介绍如何为 YOLO-Toys 开发自定义 Handler。

## Handler 接口

所有 Handler 继承自 `BaseHandler`：

```python
from app.handlers.base import BaseHandler, LoadedModel

class MyCustomHandler(BaseHandler):
    def _do_load(self, model_id: str) -> tuple:
        """加载模型和处理器"""
        # 返回 (model, processor) 元组
        pass

    def _infer_impl(
        self,
        model,
        processor,
        image,
        params: dict
    ) -> dict:
        """执行推理"""
        # 返回结果字典
        pass
```

## 开发步骤

### 1. 创建 Handler 类

```python
# app/handlers/my_handler.py
from app.handlers.base import BaseHandler

class MyModelHandler(BaseHandler):
    def _do_load(self, model_id: str) -> tuple:
        from my_library import load_model, load_processor

        model = load_model(model_id)
        processor = load_processor(model_id)

        return model, processor

    def _infer_impl(self, model, processor, image, params):
        # 预处理
        inputs = processor(image)

        # 推理
        outputs = model(**inputs)

        # 后处理
        results = self._postprocess(outputs, params)

        return results
```

### 2. 注册 Handler

在 `app/models_metadata.py` 中添加模型元数据：

```python
MODEL_METADATA = {
    "my-model-v1": ModelMeta(
        category=ModelCategory.CUSTOM,
        handler="my_handler.MyModelHandler",
        ...
    ),
}
```

### 3. 测试 Handler

```python
import pytest
from app.handlers.my_handler import MyModelHandler

def test_my_handler():
    handler = MyModelHandler(device="cpu")
    model = handler.load("my-model-v1")

    result = model.infer(test_image, {})
    assert "boxes" in result
```

## 最佳实践

1. **内存管理**：使用 `torch.no_grad()` 减少内存占用
2. **批处理**：支持多图批处理以提高吞吐量
3. **错误处理**：提供清晰的错误信息
4. **日志记录**：记录关键操作

## 示例：添加 CLIP Handler

```python
from transformers import CLIPModel, CLIPProcessor

class CLIPHandler(BaseHandler):
    def _do_load(self, model_id: str):
        model = CLIPModel.from_pretrained(model_id)
        processor = CLIPProcessor.from_pretrained(model_id)
        return model, processor

    def _infer_impl(self, model, processor, image, params):
        text = params.get("text", "")

        inputs = processor(
            text=[text],
            images=image,
            return_tensors="pt"
        )

        outputs = model(**inputs)

        return {
            "similarity": outputs.logits_per_image.item(),
            "embeddings": outputs.image_embeds.tolist()
        }
```
