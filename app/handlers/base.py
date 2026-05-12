"""
模型处理器基类 - 定义统一接口
"""

from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from app.handlers.utils import bgr_to_pil, make_result


class BaseHandler(ABC):
    """所有模型处理器的基类"""

    def __init__(self, device: str):
        self._device = device

    @property
    def device(self) -> str:
        return self._device

    # ------------------------------------------------------------------
    # 子类必须实现
    # ------------------------------------------------------------------

    @abstractmethod
    def load(self, model_id: str) -> tuple[Any, Any | None]:
        """
        加载模型，返回 (model, processor)。
        processor 可为 None（如 YOLO 不需要独立 processor）。
        """

    @abstractmethod
    def infer(
        self,
        model: Any,
        processor: Any | None,
        image: np.ndarray,
        *,
        conf: float = 0.25,
        iou: float = 0.45,
        max_det: int = 300,
        device: str | None = None,
        imgsz: int | None = None,
        half: bool = False,
        text_queries: list[str] | None = None,
        question: str | None = None,
    ) -> dict[str, Any]:
        """执行推理，返回标准结果字典"""

    # ------------------------------------------------------------------
    # 工具方法（向后兼容别名）
    # ------------------------------------------------------------------

    # 提供静态方法作为向后兼容的别名
    # 新代码应直接使用 utils.bgr_to_pil 和 utils.make_result
    bgr_to_pil = staticmethod(bgr_to_pil)
    make_result = staticmethod(make_result)

    # ------------------------------------------------------------------
    # 实例方法
    # ------------------------------------------------------------------

    def _model_to_device(self, model: Any) -> Any:
        """将模型移动到当前设备（GPU 场景）"""
        if self._device != "cpu" and hasattr(model, "to"):
            model = model.to(self._device)
        return model

    def _to_device(self, inputs: dict[str, Any], device: str | None = None) -> dict[str, Any]:
        """将 tensor dict 移动到指定设备"""
        target = device or self._device
        if target == "cpu":
            return inputs
        return {k: (v.to(target) if hasattr(v, "to") else v) for k, v in inputs.items()}
