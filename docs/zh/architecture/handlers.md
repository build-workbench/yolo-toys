# Handler 架构

Handler 模式是 YOLO-Toys 的核心扩展机制。

## Handler 接口

所有 Handler 实现共同接口：

```python
class BaseHandler:
    def load(self, model_path: str) -> None:
        """从路径加载模型"""
        pass

    def infer(self, image: np.ndarray, **kwargs) -> dict:
        """对图像进行推理"""
        pass

    def unload(self) -> None:
        """释放资源"""
        pass
```

## 现有 Handler

| Handler | 模型 | 描述 |
|---------|--------|-------------|
| YOLOHandler | yolov8n, yolov8s 等 | Ultralytics YOLO 模型 |
| DETRHandler | detr-resnet-50 | Facebook DETR |
| OWLViTHandler | owl-vit-base | OpenAI OWL-ViT |
| GroundingDINOHandler | groundingdino | Grounding DINO |
| BLIPHandler | blip-base | 图像描述 & VQA |

## 创建自定义 Handler

```python
from app.handlers.base import BaseHandler

class MyHandler(BaseHandler):
    def load(self, model_path: str) -> None:
        # 在此加载你的模型
        self.model = load_my_model(model_path)

    def infer(self, image: np.ndarray, **kwargs) -> dict:
        # 运行推理
        results = self.model(image)
        return self.format_results(results)
```

## Handler 注册

将你的 Handler 添加到注册表：

```python
HANDLER_REGISTRY = {
    "yolo": YOLOHandler,
    "detr": DETRHandler,
    "myhandler": MyHandler,  # 你的 Handler
}
```
