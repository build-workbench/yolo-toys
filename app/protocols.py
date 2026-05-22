"""
协议定义 - 定义组件间的接口协议

这些 Protocol 定义了各组件的接口边界（Seams），
允许在不修改代码的情况下替换实现（如测试时使用 mock）。
"""

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class ImageDecoder(Protocol):
    """
    图像解码器协议。

    Seam: 允许替换图像解码实现（如使用 PIL 或其他库）。
    """

    def decode(self, data: bytes) -> np.ndarray | None:
        """
        解码图像数据。

        Args:
            data: 图像字节数据

        Returns:
            解码后的图像数组（BGR 格式），解码失败返回 None
        """
        ...
