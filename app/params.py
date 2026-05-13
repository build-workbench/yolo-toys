"""
推理参数容器 - 统一参数传递接口

Deep Module 设计：
- Interface: 单一数据类，包含所有可能的推理参数
- Implementation: Handler 选择性使用所需参数
- Depth: 接口简单（一个对象），隐藏了参数验证和默认值逻辑
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class InferenceParams:
    """
    推理参数容器 - 根据模型类型选择性使用。

    这个数据类封装了所有推理相关的参数，每个 Handler 只使用其需要的参数子集。
    通过 `for_*()` 方法可以便捷地提取特定模型类型所需的参数。

    Attributes:
        conf: 置信度阈值，用于过滤低置信度检测
        iou: IoU 阈值，用于 NMS（非极大值抑制）
        max_det: 最大检测数量
        imgsz: 输入图像尺寸（仅 YOLO 使用）
        half: 是否使用半精度（FP16）推理
        device: 推理设备（cuda、mps、cpu）
        text_queries: 文本查询列表（用于开放词汇检测）
        question: 问题文本（用于 VQA）
    """

    # YOLO 参数
    conf: float = 0.25
    iou: float = 0.45
    max_det: int = 300
    imgsz: int | None = None
    half: bool = False

    # 通用参数
    device: str | None = None

    # 开放词汇检测参数
    text_queries: list[str] | None = None

    # VQA 参数
    question: str | None = None

    def for_yolo(self) -> dict[str, Any]:
        """
        提取 YOLO 相关参数。

        Returns:
            包含 YOLO 推理所需参数的字典
        """
        kwargs: dict[str, Any] = {
            "conf": self.conf,
            "iou": self.iou,
            "max_det": self.max_det,
            "device": self.device,
            "verbose": False,
        }
        if self.imgsz is not None:
            kwargs["imgsz"] = int(self.imgsz)
        if self.half and (self.device or "").startswith("cuda"):
            kwargs["half"] = True
        return kwargs

    def for_detr(self) -> dict[str, Any]:
        """
        提取 DETR 相关参数。

        Returns:
            包含 DETR 推理所需参数的字典
        """
        return {"conf": self.conf}

    def for_owlvit(self) -> dict[str, Any]:
        """
        提取 OWL-ViT 相关参数。

        Returns:
            包含 OWL-ViT 推理所需参数的字典
        """
        return {
            "conf": self.conf,
            "text_queries": self.text_queries or ["object"],
        }

    def for_grounding_dino(self) -> dict[str, Any]:
        """
        提取 Grounding DINO 相关参数。

        Returns:
            包含 Grounding DINO 推理所需参数的字典
        """
        return {
            "conf": self.conf,
            "text_queries": self.text_queries or ["object"],
        }

    def for_blip_caption(self) -> dict[str, Any]:
        """
        提取 BLIP Caption 相关参数。

        Returns:
            包含 BLIP Caption 推理所需参数的字典（当前无特定参数）
        """
        return {}

    def for_blip_vqa(self) -> dict[str, Any]:
        """
        提取 BLIP VQA 相关参数。

        Returns:
            包含 BLIP VQA 推理所需参数的字典
        """
        return {"question": self.question or "What is in this image?"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InferenceParams":
        """
        从 flat dict 创建参数对象（API 层适配器）。

        Args:
            data: 包含推理参数的字典，通常来自 API 请求

        Returns:
            InferenceParams 实例
        """
        return cls(
            conf=data.get("conf", 0.25),
            iou=data.get("iou", 0.45),
            max_det=data.get("max_det", 300),
            device=data.get("device"),
            imgsz=data.get("imgsz"),
            half=data.get("half", False),
            text_queries=data.get("text_queries"),
            question=data.get("question"),
        )
