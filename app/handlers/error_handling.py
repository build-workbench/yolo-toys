"""
推理错误处理装饰器

提供统一的错误处理和日志记录，减少重复代码。
"""

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

logger = logging.getLogger(__name__)


def handle_inference_errors(model_name: str) -> Callable:
    """
    推理错误处理装饰器

    统一处理 RuntimeError（GPU 内存不足）和通用异常，
    提供一致的日志记录和错误传播。

    Args:
        model_name: 模型名称，用于日志消息

    Usage:
        @handle_inference_errors("YOLO")
        def infer(self, model, processor, image, **kwargs):
            # 推理逻辑
            results = model(image, **kwargs)
            return results
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except RuntimeError as e:
                # CUDA out of memory 或其他运行时错误
                if "out of memory" in str(e).lower():
                    logger.error("%s GPU 内存不足: %s", model_name, e)
                else:
                    logger.error("%s 运行时错误: %s", model_name, e)
                raise
            except Exception as e:
                logger.exception("%s 推理失败: %s", model_name, e)
                raise

        return wrapper

    return decorator
