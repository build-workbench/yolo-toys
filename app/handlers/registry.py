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

# 类别显示名称
_CATEGORY_DISPLAY_NAMES = {
    ModelCategory.YOLO_DETECT: "YOLO 检测",
    ModelCategory.YOLO_SEGMENT: "YOLO 分割",
    ModelCategory.YOLO_POSE: "YOLO 姿态",
    ModelCategory.HF_DETR: "DETR 检测",
    ModelCategory.HF_OWLVIT: "开放词汇检测",
    ModelCategory.HF_GROUNDING_DINO: "Grounding DINO",
    ModelCategory.MULTIMODAL_CAPTION: "图像描述",
    ModelCategory.MULTIMODAL_VQA: "视觉问答",
}


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

    @staticmethod
    def _resolve_category(model_id: str) -> str:
        """推断模型类别"""
        info = MODEL_REGISTRY.get(model_id)
        if info:
            return info["category"]

        # 未注册的 .pt 文件按 YOLO 处理
        if model_id.endswith(".pt"):
            lower = model_id.lower()
            if "seg" in lower:
                return ModelCategory.YOLO_SEGMENT
            if "pose" in lower:
                return ModelCategory.YOLO_POSE
            return ModelCategory.YOLO_DETECT

        # 按名称模式猜测 HuggingFace 模型
        lower = model_id.lower()
        if "detr" in lower:
            return ModelCategory.HF_DETR
        if "owlvit" in lower:
            return ModelCategory.HF_OWLVIT
        if "grounding" in lower or "dino" in lower:
            return ModelCategory.HF_GROUNDING_DINO
        if "blip" in lower and "vqa" in lower:
            return ModelCategory.MULTIMODAL_VQA
        if "blip" in lower and ("caption" in lower or "captioning" in lower):
            return ModelCategory.MULTIMODAL_CAPTION

        # 含 / 的尝试作为 DETR 兜底
        if "/" in model_id:
            return ModelCategory.HF_DETR

        raise ValueError(f"Unknown model: {model_id}")


def get_available_models() -> dict[str, dict[str, Any]]:
    """获取可用模型列表，按类别分组"""
    categories: dict[str, dict[str, Any]] = {}
    for cat_key, display_name in _CATEGORY_DISPLAY_NAMES.items():
        categories[cat_key] = {"name": display_name, "models": []}

    for model_id, info in MODEL_REGISTRY.items():
        cat = info.get("category", "")
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

    return {k: v for k, v in categories.items() if v["models"]}


def get_model_info(model_id: str) -> dict[str, Any] | None:
    """获取模型信息"""
    return MODEL_REGISTRY.get(model_id)
