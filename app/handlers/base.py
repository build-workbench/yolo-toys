"""
模型处理器基类 - 定义统一接口
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from app.handlers.utils import bgr_to_pil, make_result

if TYPE_CHECKING:
    import numpy as np

    from app.config_protocols import HandlerConfig
    from app.params import InferenceParams


def _auto_detect_device() -> str:
    """自动检测最佳设备（cuda/mps/cpu）"""
    try:
        import torch

        if hasattr(torch, "cuda") and torch.cuda.is_available():
            return "cuda:0"
        if (
            hasattr(torch, "backends")
            and hasattr(torch.backends, "mps")
            and torch.backends.mps.is_available()
        ):
            return "mps"
    except ImportError:
        pass
    return "cpu"


class LoadedModel:
    """
    封装已加载的模型，隐藏 processor 细节。

    Deep Module 设计：
    - Interface: 单一 infer() 方法
    - Implementation: 隐藏 model、processor、handler 的协调
    - Depth: 调用者无需了解 processor 的存在
    """

    def __init__(
        self,
        model: Any,
        processor: Any | None,
        handler: BaseHandler,
        model_id: str,
    ):
        self._model = model
        self._processor = processor
        self._handler = handler
        self._model_id = model_id

    def infer(self, image: np.ndarray, params: InferenceParams) -> dict[str, Any]:
        """
        执行推理。

        Args:
            image: 输入图像（BGR 格式）
            params: 推理参数

        Returns:
            推理结果字典
        """
        # 调用公开方法，恢复封装（而非私有 _infer_impl）
        return self._handler.infer(self._model, self._processor, image, params)

    @property
    def model_id(self) -> str:
        """获取模型 ID"""
        return self._model_id

    @property
    def model(self) -> Any:
        """获取底层模型对象（用于高级用途）"""
        return self._model

    @property
    def processor(self) -> Any | None:
        """获取底层 processor 对象（用于高级用途）"""
        return self._processor


class BaseHandler(ABC):
    """所有模型处理器的基类"""

    def __init__(
        self,
        config: HandlerConfig | str | None = None,
        *,
        device: str | None = None,
    ):
        """
        初始化 Handler。

        Args:
            config: Handler 配置对象或设备字符串（向后兼容）
            device: 设备字符串（向后兼容关键字参数）

        支持以下调用方式：
            - Handler(config_obj)
            - Handler("cuda:0")
            - Handler(device="cuda:0")
        """
        # 向后兼容：支持 device 关键字参数
        if config is None and device is not None:
            config = device
        elif config is None:
            config = _auto_detect_device()

        if isinstance(config, str):
            # 向后兼容：直接传入设备字符串
            self._device = config
            self._config = None  # type: ignore[assignment]
        else:
            self._config = config
            self._device = config.device

    @property
    def device(self) -> str:
        return self._device

    @property
    def config(self) -> HandlerConfig | None:
        """获取配置对象"""
        return self._config

    # ------------------------------------------------------------------
    # 公开接口
    # ------------------------------------------------------------------

    def load(self, model_id: str) -> LoadedModel:
        """
        加载模型，返回封装对象。

        Args:
            model_id: 模型标识符

        Returns:
            LoadedModel 封装对象
        """
        model, processor = self._do_load(model_id)
        return LoadedModel(model, processor, self, model_id)

    # ------------------------------------------------------------------
    # 子类必须实现
    # ------------------------------------------------------------------

    @abstractmethod
    def _do_load(self, model_id: str) -> tuple[Any, Any | None]:
        """
        执行实际的模型加载。

        Args:
            model_id: 模型标识符

        Returns:
            (model, processor) 元组，processor 可为 None
        """

    @abstractmethod
    def _infer_impl(
        self,
        model: Any,
        processor: Any | None,
        image: np.ndarray,
        params: InferenceParams,
    ) -> dict[str, Any]:
        """
        执行实际的推理。

        Args:
            model: 模型对象
            processor: 处理器对象（可为 None）
            image: 输入图像
            params: 推理参数

        Returns:
            推理结果字典
        """

    # ------------------------------------------------------------------
    # 向后兼容：保留旧的抽象方法签名作为别名
    # ------------------------------------------------------------------

    def infer(
        self,
        model: Any,
        processor: Any | None,
        image: np.ndarray,
        params: InferenceParams,
    ) -> dict[str, Any]:
        """
        执行推理（向后兼容别名）。

        新代码应使用 LoadedModel.infer() 方法。
        """
        return self._infer_impl(model, processor, image, params)

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
