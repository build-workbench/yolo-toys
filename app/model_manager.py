"""
多模型管理器 - 策略模式重构版

使用 HandlerRegistry + BaseHandler 体系替代原有的 if/elif 链式调用，
每种模型类型的加载和推理逻辑被封装在独立的 Handler 中。
本模块仅保留面向上层（main.py / tests）的公共 API。
"""

import gc
import logging
import threading
import time
import urllib.parse
from contextlib import contextmanager
from typing import Any

import numpy as np
from cachetools import TTLCache

from app.config_adapters import SettingsModelManagerConfig
from app.config_protocols import ModelManagerConfig
from app.handlers.base import LoadedModel
from app.handlers.registry import HandlerRegistry
from app.params import InferenceParams

logger = logging.getLogger(__name__)

try:
    import torch
except ImportError:
    torch = None


def get_memory_usage() -> float:
    """获取当前内存使用比例，用于缓存清理决策"""
    try:
        import psutil

        return psutil.virtual_memory().percent / 100
    except ImportError:
        return 0.0


class ModelCache(TTLCache):
    """带内存监控和线程安全的 TTL 缓存"""

    def __init__(self, maxsize: int, ttl: float, memory_threshold: float = 0.85):
        super().__init__(maxsize=maxsize, ttl=ttl)
        self._access_times: dict[str, float] = {}
        self._lock = threading.Lock()
        self._memory_threshold = memory_threshold

    @contextmanager
    def _threadsafe(self):
        """线程安全上下文管理器"""
        self._lock.acquire()
        try:
            yield
        finally:
            self._lock.release()

    def __getitem__(self, key: str) -> Any:
        with self._lock:
            value = super().__getitem__(key)
            self._access_times[key] = time.time()
            return value

    def __setitem__(self, key: str, value: Any) -> None:
        with self._lock:
            # 内存压力检查
            if len(self) >= self.maxsize or get_memory_usage() > self._memory_threshold:
                self._evict_lru_unsafe()
            super().__setitem__(key, value)
            self._access_times[key] = time.time()

    def __delitem__(self, key: str) -> None:
        with self._lock:
            super().__delitem__(key)
            self._access_times.pop(key, None)

    def _evict_lru_unsafe(self) -> None:
        """驱逐最久未使用的模型（内部方法，需在锁内调用）"""
        if not self._access_times:
            return
        oldest_key = min(self._access_times, key=lambda cache_key: self._access_times[cache_key])
        logger.warning("内存压力，驱逐模型缓存: %s", oldest_key)
        self.pop(oldest_key, None)
        self._access_times.pop(oldest_key, None)
        # 尝试垃圾回收
        gc.collect()
        if torch is not None and torch.cuda.is_available():
            torch.cuda.empty_cache()

    def _evict_lru(self) -> None:
        """驱逐最久未使用的模型（线程安全）"""
        with self._lock:
            self._evict_lru_unsafe()


class ModelManager:
    """统一模型管理器 - 委托 HandlerRegistry 完成加载和推理"""

    def __init__(self, config: ModelManagerConfig | None = None):
        """
        初始化 ModelManager。

        Args:
            config: ModelManager 配置对象。如果为 None，从 AppSettings 自动构建。
        """
        if config is None:
            from app.config import get_settings

            settings = get_settings()
            config = SettingsModelManagerConfig(settings)

        self._config = config
        self._device = config.device
        self._registry = HandlerRegistry(config.device)  # 向后兼容：传递设备字符串
        # 使用 LRU + TTL 混合缓存
        self._cache = ModelCache(
            maxsize=config.cache_maxsize,
            ttl=config.cache_ttl,
            memory_threshold=config.memory_threshold,
        )
        self._load_times: dict[str, float] = {}
        self._access_count: dict[str, int] = {}

    @property
    def device(self) -> str:
        return self._device

    @property
    def cache(self) -> "ModelCache":
        """访问模型缓存（只读）"""
        return self._cache

    @property
    def cache_info(self) -> dict[str, Any]:
        """获取缓存统计信息"""
        return {
            "cache_size": len(self._cache),
            "cache_maxsize": self._cache.maxsize,
            "cache_ttl": self._cache.ttl,
            "cached_models": list(self._cache.keys()),
            "memory_usage": get_memory_usage(),
        }

    def clear_cache(self) -> None:
        """清空模型缓存"""
        cleared = len(self._cache)
        self._cache.clear()
        self._access_count.clear()
        gc.collect()
        if torch is not None and torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info("模型缓存已清空: %d 个模型", cleared)

    def load_model(self, model_id: str) -> LoadedModel:
        """加载模型（带缓存），返回封装对象

        Args:
            model_id: 模型标识符

        Returns:
            LoadedModel 封装对象

        Raises:
            ValueError: 模型 ID 包含非法字符
        """
        # 安全验证：防止路径遍历攻击（包括 URL 编码绕过）
        if not model_id or not isinstance(model_id, str):
            raise ValueError("Model ID must be a non-empty string")

        # 解码 URL 编码后再次检查
        decoded_id = urllib.parse.unquote(model_id)
        forbidden_patterns = ["../", "..\\", "/", "\\", "\x00"]
        for pattern in forbidden_patterns:
            if pattern in model_id or pattern in decoded_id:
                raise ValueError("Invalid model ID: contains forbidden character sequence")

        if model_id in self._cache:
            self._access_count[model_id] = self._access_count.get(model_id, 0) + 1
            return self._cache[model_id]

        # 记录加载时间
        start_time = time.time()
        handler = self._registry.get_handler(model_id)
        loaded = handler.load(model_id)
        load_time = time.time() - start_time

        self._cache[model_id] = loaded
        self._load_times[model_id] = load_time
        self._access_count[model_id] = 1

        logger.info(
            "模型已加载: %s (handler=%s, load_time=%.2fs)",
            model_id,
            type(handler).__name__,
            load_time,
        )
        return loaded

    def infer(
        self,
        *,
        model_id: str,
        image: np.ndarray,
        params: InferenceParams | None = None,
        # 向后兼容：支持 flat 参数
        conf: float = 0.25,
        iou: float = 0.45,
        max_det: int = 300,
        device: str | None = None,
        imgsz: int | None = None,
        half: bool = False,
        text_queries: list[str] | None = None,
        question: str | None = None,
    ) -> dict[str, Any]:
        """统一推理接口 - 自动路由到对应 Handler

        Args:
            model_id: 模型标识符
            image: 输入图像（BGR 格式）
            params: 推理参数对象（推荐使用）
            conf: 置信度阈值（向后兼容）
            iou: IoU 阈值（向后兼容）
            max_det: 最大检测数量（向后兼容）
            device: 推理设备（向后兼容）
            imgsz: 输入图像尺寸（向后兼容）
            half: 是否使用半精度（向后兼容）
            text_queries: 文本查询列表（向后兼容）
            question: 问题文本（向后兼容）

        Returns:
            推理结果字典
        """
        # 向后兼容：如果未提供 params，从 flat 参数构建
        if params is None:
            params = InferenceParams(
                conf=conf,
                iou=iou,
                max_det=max_det,
                device=device,
                imgsz=imgsz,
                half=half,
                text_queries=text_queries,
                question=question,
            )

        # 加载模型并执行推理
        loaded = self.load_model(model_id)
        return loaded.infer(image, params)

    def get_stats(self) -> dict[str, Any]:
        """获取管理器统计信息"""
        return {
            "device": self._device,
            "cache_info": self.cache_info,
            "model_stats": {
                model_id: {
                    "load_time": self._load_times.get(model_id, 0),
                    "access_count": self._access_count.get(model_id, 0),
                }
                for model_id in self._cache
            },
        }


# 全局模型管理器实例
model_manager = ModelManager()
