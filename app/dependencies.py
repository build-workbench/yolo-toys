"""
FastAPI 依赖注入 - 提供组件的依赖注入支持

将全局单例改为依赖注入模式，提升测试性和可维护性。
"""

import asyncio
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

if TYPE_CHECKING:
    from app.model_manager import ModelManager
    from app.protocols import ImageDecoder


# ======================================================================
# ConcurrencyControl
# ======================================================================


class ConcurrencyControl:
    """
    并发控制 - 封装 asyncio.Semaphore 提供更清晰的接口

    Seam: 允许替换并发控制实现（如使用分布式信号量）
    """

    def __init__(self, max_concurrency: int):
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._max_concurrency = max_concurrency

    @asynccontextmanager
    async def acquire(self):
        """获取并发槽位，使用完毕后自动释放"""
        async with self._semaphore:
            yield

    @property
    def max_concurrency(self) -> int:
        """最大并发数"""
        return self._max_concurrency


# ======================================================================
# 依赖注入工厂
# ======================================================================


@lru_cache
def get_model_manager() -> "ModelManager":
    """
    获取 ModelManager 单例（通过依赖注入）。

    使用 lru_cache 确保进程内只有一个实例。
    测试时可以通过 Depends 覆盖。
    """
    from app.config import get_settings
    from app.config_adapters import SettingsModelManagerConfig
    from app.model_manager import ModelManager

    settings = get_settings()
    config = SettingsModelManagerConfig(settings)
    return ModelManager(config)


@lru_cache
def get_concurrency_control() -> ConcurrencyControl:
    """
    获取 ConcurrencyControl 单例。

    使用 lru_cache 确保进程内只有一个实例。
    """
    from app.config import get_settings

    settings = get_settings()
    return ConcurrencyControl(settings.max_concurrency)


@lru_cache
def get_image_decoder() -> "ImageDecoder":
    """
    获取 ImageDecoder 单例。

    使用 lru_cache 确保进程内只有一个实例。
    """
    from app.decoders import OpenCVDecoder

    return OpenCVDecoder()


# ======================================================================
# 类型别名（用于依赖注入）
# ======================================================================

ModelManagerDep = Annotated["ModelManager", Depends(get_model_manager)]
ConcurrencyDep = Annotated[ConcurrencyControl, Depends(get_concurrency_control)]
ImageDecoderDep = Annotated["ImageDecoder", Depends(get_image_decoder)]
