"""
模型注册表 - 管理模型处理器映射

支持动态注册 Handler，允许运行时扩展和测试替换。
"""

from typing import TYPE_CHECKING, Any

from app.handlers.base import BaseHandler
from app.models_metadata import MODEL_REGISTRY, ModelCategory

if TYPE_CHECKING:
    from app.config_protocols import HandlerConfig


class HandlerRegistry:
    """处理器注册表 - 根据模型 ID 获取对应 Handler

    支持动态注册 Handler，允许运行时扩展和测试替换。
    """

    # 默认类别 → 处理器类映射（使用 None 延迟初始化）
    _default_handlers: dict[ModelCategory, type[BaseHandler]] | None = None

    def __init__(self, config_or_device: "HandlerConfig | str"):
        """
        初始化注册表。

        Args:
            config_or_device: HandlerConfig 对象或设备字符串（向后兼容）
        """
        self._config_or_device = config_or_device
        self._handler_cache: dict[str, BaseHandler] = {}
        self._custom_handlers: dict[ModelCategory, type[BaseHandler]] = {}

        # 延迟导入以避免循环依赖，只初始化一次
        if HandlerRegistry._default_handlers is None:
            from app.handlers.blip_handler import BLIPCaptionHandler, BLIPVQAHandler
            from app.handlers.hf_handler import DETRHandler, GroundingDINOHandler, OWLViTHandler
            from app.handlers.yolo_handler import YOLOHandler

            HandlerRegistry._default_handlers = {
                ModelCategory.YOLO_DETECT: YOLOHandler,
                ModelCategory.YOLO_SEGMENT: YOLOHandler,
                ModelCategory.YOLO_POSE: YOLOHandler,
                ModelCategory.HF_DETR: DETRHandler,
                ModelCategory.HF_OWLVIT: OWLViTHandler,
                ModelCategory.HF_GROUNDING_DINO: GroundingDINOHandler,
                ModelCategory.MULTIMODAL_CAPTION: BLIPCaptionHandler,
                ModelCategory.MULTIMODAL_VQA: BLIPVQAHandler,
            }

    def register_handler(self, category: ModelCategory, handler_cls: type[BaseHandler]) -> None:
        """
        动态注册 Handler。

        Args:
            category: 模型类别
            handler_cls: Handler 类

        注册后会清除缓存，确保使用新的 Handler。
        """
        self._custom_handlers[category] = handler_cls
        self._handler_cache.clear()

    def unregister_handler(self, category: ModelCategory) -> bool:
        """
        移除自定义注册的 Handler。

        Args:
            category: 模型类别

        Returns:
            是否成功移除
        """
        if category in self._custom_handlers:
            del self._custom_handlers[category]
            self._handler_cache.clear()
            return True
        return False

    def get_handler(self, model_id: str) -> BaseHandler:
        """获取模型对应的处理器实例（带缓存）"""
        category = self._resolve_category(model_id)
        # 优先使用自定义注册，然后是默认映射
        default_handlers = self._default_handlers or {}
        handler_cls = self._custom_handlers.get(category) or default_handlers.get(category)
        if handler_cls is None:
            raise ValueError(f"Unknown model category for {model_id}")

        cls_name = handler_cls.__name__
        if cls_name not in self._handler_cache:
            # 传递 config 或 device 给 Handler（向后兼容）
            self._handler_cache[cls_name] = handler_cls(self._config_or_device)
        return self._handler_cache[cls_name]

    def _resolve_category(self, model_id: str) -> ModelCategory:
        """推断模型类别"""
        return ModelCategory.infer_from_id(model_id, MODEL_REGISTRY)

    @classmethod
    def get_default_handlers(cls) -> dict[ModelCategory, type[BaseHandler]]:
        """获取默认 Handler 映射（只读）"""
        return (cls._default_handlers or {}).copy()


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
