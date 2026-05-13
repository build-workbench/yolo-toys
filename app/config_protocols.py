"""
配置协议定义 - 用于依赖注入

这些 Protocol 定义了各组件所需的配置接口，
允许在不修改代码的情况下替换配置来源（如测试时使用 mock 配置）。
"""

from typing import Protocol


class HandlerConfig(Protocol):
    """
    Handler 配置协议。

    定义了 Handler 所需的配置属性。
    """

    @property
    def device(self) -> str:
        """推理设备（cuda、mps、cpu）"""
        ...

    @property
    def blip_max_tokens(self) -> int:
        """BLIP 模型生成的最大 token 数"""
        ...

    @property
    def grounding_text_threshold(self) -> float:
        """Grounding DINO 文本阈值"""
        ...


class ModelManagerConfig(Protocol):
    """
    ModelManager 配置协议。

    定义了 ModelManager 所需的配置属性。
    """

    @property
    def cache_maxsize(self) -> int:
        """模型缓存最大数量"""
        ...

    @property
    def cache_ttl(self) -> int:
        """模型缓存 TTL（秒）"""
        ...

    @property
    def memory_threshold(self) -> float:
        """内存使用阈值（触发缓存清理）"""
        ...

    @property
    def device(self) -> str:
        """推理设备"""
        ...
