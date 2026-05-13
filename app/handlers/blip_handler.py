"""
BLIP 多模态模型处理器 - 图像描述 / 视觉问答
"""

import logging
import time
from typing import Any

import numpy as np

from app.config import get_settings
from app.handlers.base import BaseHandler
from app.handlers.error_handling import handle_inference_errors
from app.handlers.hf_handler import _require_hf
from app.params import InferenceParams

try:
    import torch
except ImportError:
    torch = None

logger = logging.getLogger(__name__)
settings = get_settings()


def _require_torch() -> Any:
    """Return torch module when available."""
    if torch is None:
        raise RuntimeError("torch not installed")
    return torch


class BLIPCaptionHandler(BaseHandler):
    """BLIP 图像描述生成"""

    def _do_load(self, model_id: str) -> tuple[Any, Any]:
        _require_hf()
        from transformers import BlipForConditionalGeneration, BlipProcessor

        processor = BlipProcessor.from_pretrained(model_id)
        model = BlipForConditionalGeneration.from_pretrained(model_id)
        model = self._model_to_device(model)
        return model, processor

    def _infer_impl(
        self,
        model: Any,
        processor: Any,
        image: np.ndarray,
        params: InferenceParams,
    ) -> dict[str, Any]:
        t0 = time.time()
        torch_module = _require_torch()
        pil_image = self.bgr_to_pil(image)

        inputs = processor(pil_image, return_tensors="pt")
        inputs = self._to_device(inputs)

        out = self._call_model_blip_caption(torch_module, model, inputs)

        caption = processor.decode(out[0], skip_special_tokens=True)
        elapsed = (time.time() - t0) * 1000.0

        return self.make_result(image, inference_time=elapsed, task="caption", caption=caption)

    @staticmethod
    @handle_inference_errors("BLIP Caption")
    def _call_model_blip_caption(torch_module: Any, model: Any, inputs: dict[str, Any]) -> Any:
        """调用 BLIP Caption 模型推理（带统一错误处理）"""
        with torch_module.no_grad():
            return model.generate(**inputs, max_new_tokens=settings.blip_max_tokens)


class BLIPVQAHandler(BaseHandler):
    """BLIP 视觉问答"""

    def _do_load(self, model_id: str) -> tuple[Any, Any]:
        _require_hf()
        from transformers import BlipForQuestionAnswering, BlipProcessor

        processor = BlipProcessor.from_pretrained(model_id)
        model = BlipForQuestionAnswering.from_pretrained(model_id)
        model = self._model_to_device(model)
        return model, processor

    def _infer_impl(
        self,
        model: Any,
        processor: Any,
        image: np.ndarray,
        params: InferenceParams,
    ) -> dict[str, Any]:
        t0 = time.time()
        torch_module = _require_torch()
        vqa_params = params.for_blip_vqa()
        q = vqa_params["question"]
        pil_image = self.bgr_to_pil(image)

        inputs = processor(pil_image, q, return_tensors="pt")
        inputs = self._to_device(inputs)

        out = self._call_model_blip_vqa(torch_module, model, inputs)

        answer = processor.decode(out[0], skip_special_tokens=True)
        elapsed = (time.time() - t0) * 1000.0

        return self.make_result(
            image, inference_time=elapsed, task="vqa", question=q, answer=answer
        )

    @staticmethod
    @handle_inference_errors("BLIP VQA")
    def _call_model_blip_vqa(torch_module: Any, model: Any, inputs: dict[str, Any]) -> Any:
        """调用 BLIP VQA 模型推理（带统一错误处理）"""
        with torch_module.no_grad():
            return model.generate(**inputs, max_new_tokens=settings.blip_max_tokens)
