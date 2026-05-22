"""
图像解码器实现 - 提供具体的图像解码实现
"""

import cv2
import numpy as np

from app.protocols import ImageDecoder


class OpenCVDecoder(ImageDecoder):
    """
    OpenCV 图像解码器。

    使用 cv2.imdecode 解码图像数据。
    """

    def decode(self, data: bytes) -> np.ndarray | None:
        """
        解码图像数据。

        Args:
            data: 图像字节数据

        Returns:
            解码后的图像数组（BGR 格式），解码失败返回 None
        """
        if not data:
            return None
        nparr = np.frombuffer(data, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
