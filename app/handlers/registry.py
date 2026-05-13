"""
模型注册表 - 管理模型处理器映射
"""

from typing import Any

from app.handlers.base import BaseHandler
from app.handlers.blip_handler import BLIPCaptionHandler, BLIPVQAHandler
from app.handlers.hf_handler import DETRHandler, GroundingDINOHandler, OWLViTHandler
from app.handlers.yolo_handler import YOLOHandler
from app.models_metadata import MODEL_REGISTRY, ModelCategory

# 类别 → 处理器类映射
_CATEGORY_HANDLER_MAP = {
    ModelCategory.YOLO_DETECT: YOLOHandler,
    ModelCategory.YOLO_SEGMENT: YOLOHandler,
    ModelCategory.YOLO_POSE: YOLOHandler,
    ModelCategory.HF_DETR: DETRHandler,
    ModelCategory.HF_OWLVIT: OWLViTHandler,
    ModelCategory.HF_GROUNDING_DINO: GroundingDINOHandler,
    ModelCategory.MULTIMODAL_CAPTION: BLIPCaptionHandler,
    ModelCategory.MULTIMODAL_VQA: BLIPVQAHandler,
}

# 类别显示名称（使用枚举的 display_name 属性）
# 保留此映射用于向后兼容，但优先使用 ModelCategory.display_name


class HandlerRegistry:
    """处理器注册表 - 根据模型 ID 获取对应 Handler"""

    def __init__(self, device: str):
        self._device = device
        self._handler_cache: dict[str, BaseHandler] = {}

    def get_handler(self, model_id: str) -> BaseHandler:
        """获取模型对应的处理器实例（带缓存）"""
        category = self._resolve_category(model_id)
        handler_cls = _CATEGORY_HANDLER_MAP.get(category)
        if handler_cls is None:
            raise ValueError(f"Unknown model category for {model_id}")

        cls_name = handler_cls.__name__
        if cls_name not in self._handler_cache:
            self._handler_cache[cls_name] = handler_cls(self._device)
        return self._handler_cache[cls_name]

    def _resolve_category(self, model_id: str) -> ModelCategory:
        """推断模型类别"""
        return ModelCategory.infer_from_id(model_id, MODEL_REGISTRY)


def get_available_models() -> dict[str, dict[str, Any]]:
    """获取可用模型列表，按类别分组"""
    categories: dict[ModelCategory, dict[str, Any]] = {}
    for cat in ModelCategory:
        categories[cat] = {"name": cat.display_name, "models": []}

    for model_id, info in MODEL_REGISTRY.items():
        cat = info.get("category")
        if cat in categories:
            categories[cat]["models"].append(
                {
                    "id": model_id,
                    "name": info.get("name", model_id),
                    "description": info.get("description", ""),
                    "speed": info.get("speed", ""),
                    "accuracy": info.get("accuracy", ""),
                }
            )

    # 返回时使用枚举的 value_str 作为键（向后兼容）
    return {cat.value_str: data for cat, data in categories.items() if data["models"]}


def get_model_info(model_id: str) -> dict[str, Any] | None:
    """获取模型信息"""
    return MODEL_REGISTRY.get(model_id)
