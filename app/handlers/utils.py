"""
Handler 工具函数

提供图像格式转换和结果构建的独立工具函数。
"""

from typing import Any

import numpy as np
from PIL import Image


def bgr_to_pil(image: np.ndarray) -> Image.Image:
    """
    OpenCV BGR ndarray → PIL RGB Image

    Args:
        image: OpenCV 格式的 BGR 图像数组 (H, W, 3)

    Returns:
        PIL RGB Image 对象

    Example:
        >>> import cv2
        >>> bgr_img = cv2.imread("image.jpg")
        >>> pil_img = bgr_to_pil(bgr_img)
    """
    return Image.fromarray(image[:, :, ::-1])


def make_result(
    image: np.ndarray,
    *,
    detections: list[dict[str, Any]] | None = None,
    inference_time: float,
    task: str = "detect",
    **extra,
) -> dict[str, Any]:
    """
    构造标准推理结果字典

    Args:
        image: 输入图像数组，用于提取宽高信息
        detections: 检测结果列表（可选）
        inference_time: 推理耗时（毫秒）
        task: 任务类型（detect/segment/pose/caption/vqa）
        **extra: 其他附加字段

    Returns:
        标准格式的结果字典，包含：
        - width: 图像宽度
        - height: 图像高度
        - inference_time: 推理耗时
        - task: 任务类型
        - detections: 检测结果（如果提供）
        - 其他附加字段

    Example:
        >>> result = make_result(
        ...     image,
        ...     detections=[{"bbox": [0, 0, 100, 100], "score": 0.9}],
        ...     inference_time=15.3,
        ...     task="detect"
        ... )
    """
    h, w = image.shape[:2]
    result: dict[str, Any] = {
        "width": w,
        "height": h,
        "inference_time": inference_time,
        "task": task,
    }
    if detections is not None:
        result["detections"] = detections
    result.update(extra)
    return result
