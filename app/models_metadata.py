"""
模型元数据注册表

包含所有支持模型的元数据，包括名称、描述、速度、精度等信息。
用于 API 端点展示和模型选择。
"""

from typing import Any


class ModelCategory:
    """模型类别常量"""

    YOLO_DETECT = "yolo_detect"
    YOLO_SEGMENT = "yolo_segment"
    YOLO_POSE = "yolo_pose"
    HF_DETR = "hf_detr"
    HF_OWLVIT = "hf_owlvit"
    HF_GROUNDING_DINO = "hf_grounding_dino"
    MULTIMODAL_CAPTION = "multimodal_caption"
    MULTIMODAL_VQA = "multimodal_vqa"


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
