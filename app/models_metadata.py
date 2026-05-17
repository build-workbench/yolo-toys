"""
模型元数据注册表

包含所有支持模型的元数据，包括名称、描述、速度、精度等信息。
用于 API 端点展示和模型选择。
"""

from enum import Enum, auto
from typing import Any


class ModelCategory(Enum):
    """
    模型类别枚举 - 封装类别推断逻辑。

    Deep Module 设计：
    - Interface: 枚举值 + infer_from_id() 方法
    - Implementation: 封装所有推断规则和回退逻辑
    - Depth: 调用者无需了解推断细节
    """

    YOLO_DETECT = auto()
    YOLO_SEGMENT = auto()
    YOLO_POSE = auto()
    HF_DETR = auto()
    HF_OWLVIT = auto()
    HF_GROUNDING_DINO = auto()
    MULTIMODAL_CAPTION = auto()
    MULTIMODAL_VQA = auto()

    @classmethod
    def infer_from_id(
        cls, model_id: str, registry: dict[str, Any] | None = None
    ) -> "ModelCategory":
        """
        从模型 ID 推断类别。

        Args:
            model_id: 模型标识符
            registry: 可选的模型注册表，用于查找已注册模型的类别

        Returns:
            推断的 ModelCategory 枚举值

        Raises:
            ValueError: 无法推断模型类别
        """
        # 如果提供了注册表，优先使用
        if registry and model_id in registry:
            cat = registry[model_id].get("category")
            # 处理枚举类型
            if isinstance(cat, cls):
                return cat
            # 处理旧的字符串类别（向后兼容）
            if isinstance(cat, str):
                return cls._from_string(cat)
            return cat

        # 未注册的 .pt 文件按 YOLO 处理
        if model_id.endswith(".pt"):
            lower = model_id.lower()
            if "seg" in lower:
                return cls.YOLO_SEGMENT
            if "pose" in lower:
                return cls.YOLO_POSE
            return cls.YOLO_DETECT

        # HuggingFace 模型推断
        lower = model_id.lower()
        if "detr" in lower:
            return cls.HF_DETR
        if "owlvit" in lower:
            return cls.HF_OWLVIT
        if "grounding" in lower or "dino" in lower:
            return cls.HF_GROUNDING_DINO
        if "blip" in lower and "vqa" in lower:
            return cls.MULTIMODAL_VQA
        if "blip" in lower and ("caption" in lower or "captioning" in lower):
            return cls.MULTIMODAL_CAPTION

        # 含 / 的尝试作为 DETR 兜底
        if "/" in model_id:
            return cls.HF_DETR

        raise ValueError(f"Unknown model: {model_id}")

    @classmethod
    def _from_string(cls, s: str) -> "ModelCategory":
        """从旧字符串格式转换（向后兼容）"""
        mapping = {
            "yolo_detect": cls.YOLO_DETECT,
            "yolo_segment": cls.YOLO_SEGMENT,
            "yolo_pose": cls.YOLO_POSE,
            "hf_detr": cls.HF_DETR,
            "hf_owlvit": cls.HF_OWLVIT,
            "hf_grounding_dino": cls.HF_GROUNDING_DINO,
            "multimodal_caption": cls.MULTIMODAL_CAPTION,
            "multimodal_vqa": cls.MULTIMODAL_VQA,
        }
        if s not in mapping:
            raise ValueError(f"Unknown category: {s}")
        return mapping[s]

    @property
    def display_name(self) -> str:
        """获取显示名称"""
        names = {
            self.YOLO_DETECT: "YOLO 检测",
            self.YOLO_SEGMENT: "YOLO 分割",
            self.YOLO_POSE: "YOLO 姿态",
            self.HF_DETR: "DETR 检测",
            self.HF_OWLVIT: "开放词汇检测",
            self.HF_GROUNDING_DINO: "Grounding DINO",
            self.MULTIMODAL_CAPTION: "图像描述",
            self.MULTIMODAL_VQA: "视觉问答",
        }
        return names.get(self, str(self))

    # 向后兼容：提供字符串值属性
    @property
    def value_str(self) -> str:
        """获取字符串值（向后兼容）"""
        mapping = {
            self.YOLO_DETECT: "yolo_detect",
            self.YOLO_SEGMENT: "yolo_segment",
            self.YOLO_POSE: "yolo_pose",
            self.HF_DETR: "hf_detr",
            self.HF_OWLVIT: "hf_owlvit",
            self.HF_GROUNDING_DINO: "hf_grounding_dino",
            self.MULTIMODAL_CAPTION: "multimodal_caption",
            self.MULTIMODAL_VQA: "multimodal_vqa",
        }
        return mapping.get(self, str(self))


# 模型注册表：模型 ID → 元数据
MODEL_REGISTRY: dict[str, dict[str, Any]] = {
    # YOLO 检测
    "yolov8n.pt": {
        "category": ModelCategory.YOLO_DETECT,
        "name": "YOLOv8 Nano",
        "description": "超轻量检测模型，适合实时场景，速度最快",
        "speed": "极快",
        "accuracy": "中等",
    },
    "yolov8s.pt": {
        "category": ModelCategory.YOLO_DETECT,
        "name": "YOLOv8 Small",
        "description": "轻量检测模型，平衡速度与精度",
        "speed": "快",
        "accuracy": "较好",
    },
    "yolov8m.pt": {
        "category": ModelCategory.YOLO_DETECT,
        "name": "YOLOv8 Medium",
        "description": "中等规模检测模型，精度更高",
        "speed": "中等",
        "accuracy": "高",
    },
    "yolov8l.pt": {
        "category": ModelCategory.YOLO_DETECT,
        "name": "YOLOv8 Large",
        "description": "大规模检测模型，高精度",
        "speed": "较慢",
        "accuracy": "很高",
    },
    "yolov8x.pt": {
        "category": ModelCategory.YOLO_DETECT,
        "name": "YOLOv8 XLarge",
        "description": "超大规模检测模型，最高精度",
        "speed": "慢",
        "accuracy": "最高",
    },
    # YOLO 分割
    "yolov8n-seg.pt": {
        "category": ModelCategory.YOLO_SEGMENT,
        "name": "YOLOv8 Nano Seg",
        "description": "超轻量实例分割模型",
        "speed": "极快",
        "accuracy": "中等",
    },
    "yolov8s-seg.pt": {
        "category": ModelCategory.YOLO_SEGMENT,
        "name": "YOLOv8 Small Seg",
        "description": "轻量实例分割模型",
        "speed": "快",
        "accuracy": "较好",
    },
    "yolov8m-seg.pt": {
        "category": ModelCategory.YOLO_SEGMENT,
        "name": "YOLOv8 Medium Seg",
        "description": "中等规模实例分割模型",
        "speed": "中等",
        "accuracy": "高",
    },
    # YOLO 姿态
    "yolov8n-pose.pt": {
        "category": ModelCategory.YOLO_POSE,
        "name": "YOLOv8 Nano Pose",
        "description": "超轻量姿态估计模型",
        "speed": "极快",
        "accuracy": "中等",
    },
    "yolov8s-pose.pt": {
        "category": ModelCategory.YOLO_POSE,
        "name": "YOLOv8 Small Pose",
        "description": "轻量姿态估计模型，检测人体关键点",
        "speed": "快",
        "accuracy": "较好",
    },
    "yolov8m-pose.pt": {
        "category": ModelCategory.YOLO_POSE,
        "name": "YOLOv8 Medium Pose",
        "description": "中等规模姿态估计模型",
        "speed": "中等",
        "accuracy": "高",
    },
    # HuggingFace DETR
    "facebook/detr-resnet-50": {
        "category": ModelCategory.HF_DETR,
        "name": "DETR ResNet-50",
        "description": "Facebook 的 DEtection TRansformer，端到端目标检测",
        "speed": "中等",
        "accuracy": "高",
    },
    "facebook/detr-resnet-101": {
        "category": ModelCategory.HF_DETR,
        "name": "DETR ResNet-101",
        "description": "DETR 大规模版本，更高精度",
        "speed": "较慢",
        "accuracy": "很高",
    },
    # OWL-ViT
    "google/owlvit-base-patch32": {
        "category": ModelCategory.HF_OWLVIT,
        "name": "OWL-ViT Base",
        "description": "开放词汇检测，可检测任意文本描述的物体",
        "speed": "中等",
        "accuracy": "高",
    },
    # Grounding DINO
    "IDEA-Research/grounding-dino-tiny": {
        "category": ModelCategory.HF_GROUNDING_DINO,
        "name": "Grounding DINO Tiny",
        "description": "先进的开放集检测模型，支持文本提示",
        "speed": "中等",
        "accuracy": "很高",
    },
    # 多模态 - 图像描述
    "Salesforce/blip-image-captioning-base": {
        "category": ModelCategory.MULTIMODAL_CAPTION,
        "name": "BLIP Caption Base",
        "description": "图像描述生成模型，自动生成图像内容描述",
        "speed": "中等",
        "accuracy": "高",
    },
    "Salesforce/blip-image-captioning-large": {
        "category": ModelCategory.MULTIMODAL_CAPTION,
        "name": "BLIP Caption Large",
        "description": "大规模图像描述模型，更丰富的描述",
        "speed": "较慢",
        "accuracy": "很高",
    },
    # 多模态 - VQA
    "Salesforce/blip-vqa-base": {
        "category": ModelCategory.MULTIMODAL_VQA,
        "name": "BLIP VQA Base",
        "description": "视觉问答模型，可回答关于图像的问题",
        "speed": "中等",
        "accuracy": "高",
    },
}
