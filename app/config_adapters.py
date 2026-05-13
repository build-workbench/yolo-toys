"""
配置适配器 - 从 AppSettings 适配到各协议

这些适配器将 AppSettings 转换为各组件所需的配置接口，
提供了配置来源的 Seam。
"""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.config import AppSettings


class SettingsHandlerConfig:
    """
    从 AppSettings 适配 Handler 配置。

    实现 HandlerConfig 协议。
    """

    def __init__(self, settings: "AppSettings"):
        self._settings = settings

    @property
    def device(self) -> str:
        """推理设备"""
        return self._settings.device or "auto"

    @property
    def blip_max_tokens(self) -> int:
        """BLIP 模型生成的最大 token 数"""
        return self._settings.blip_max_tokens

    @property
    def grounding_text_threshold(self) -> float:
        """Grounding DINO 文本阈值"""
        return self._settings.grounding_text_threshold


class SettingsModelManagerConfig:
    """
    从 AppSettings 适配 ModelManager 配置。

    实现 ModelManagerConfig 协议。
    """

    def __init__(self, settings: "AppSettings"):
        self._settings = settings
        self._cache_maxsize = int(os.getenv("MODEL_CACHE_MAXSIZE", "10"))
        self._cache_ttl = int(os.getenv("MODEL_CACHE_TTL", "3600"))
        self._memory_threshold = float(os.getenv("MODEL_MEMORY_THRESHOLD", "0.85"))

    @property
    def cache_maxsize(self) -> int:
        """模型缓存最大数量"""
        return self._cache_maxsize

    @property
    def cache_ttl(self) -> int:
        """模型缓存 TTL（秒）"""
        return self._cache_ttl

    @property
    def memory_threshold(self) -> float:
        """内存使用阈值"""
        return self._memory_threshold

    @property
    def device(self) -> str:
        """推理设备"""
        return self._settings.device or "auto"
