"""
配置适配器 - 从 AppSettings 适配到各协议

这些适配器将 AppSettings 转换为各组件所需的配置接口，
提供了配置来源的 Seam。
"""

from typing import TYPE_CHECKING

from app.handlers.base import _auto_detect_device

if TYPE_CHECKING:
    from app.config import AppSettings


def _resolve_device(device_setting: str | None) -> str:
    """解析设备设置，返回实际设备

    Args:
        device_setting: 设备设置字符串，可为 None 表示自动选择

    Returns:
        实际设备字符串（cuda:0/mps/cpu）
    """
    if device_setting:
        return device_setting
    return _auto_detect_device()


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
        return _resolve_device(self._settings.device)

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

    @property
    def cache_maxsize(self) -> int:
        """模型缓存最大数量"""
        return self._settings.model_cache_maxsize

    @property
    def cache_ttl(self) -> int:
        """模型缓存 TTL（秒）"""
        return self._settings.model_cache_ttl

    @property
    def memory_threshold(self) -> float:
        """内存使用阈值"""
        return self._settings.model_memory_threshold

    @property
    def device(self) -> str:
        """推理设备"""
        return _resolve_device(self._settings.device)
