# 配置注入

YOLO-Toys 使用一套**分层配置系统**，它将声明式设置（运维人员想要的）与程序化配置（运行时需要的）分离开来。这种分离使系统可测试、可感知环境，并且能安全地演进。

## 设计理念

配置栈遵循三条原则：

1. **Pydantic 优先**：所有设置都是经验证的 schema，而不是原始字典
2. **环境感知**：`.env` 文件、环境变量和程序化覆盖可以干净地共存
3. **协议驱动**：内部模块依赖的是协议（接口），而不是具体的设置类

## 设置层级

配置按照以下优先级顺序解析（从高到低）：

```
1. Programmatic arguments passed at initialization
2. Environment variables (e.g., YOLOTOYS_DEVICE=cuda:0)
3. .env file in the working directory
4. Default values defined in Pydantic model
```

## 三层配置

### 第一层：AppSettings（声明式）

```python
class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="YOLOTOYS_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    device: str = "auto"
    cache_maxsize: int = 3
    cache_ttl: int = 3600
    memory_threshold: float = 0.85
    log_level: str = "INFO"
    max_concurrency: int = 4
    origins_list: list[str] = ["*"]
```

这是**面向运维人员**的层。运维人员通过设置环境变量或编辑 `.env` 来改变行为。

### 第二层：Protocols（契约）

```python
class ModelManagerConfig(Protocol):
    device: str
    cache_maxsize: int
    cache_ttl: float
    memory_threshold: float
```

协议定义的是**组件需要什么**，而不是值来自哪里。这是可测试性的关键：单元测试可以传入假的配置对象，而无需触碰真实的设置基础设施。

### 第三层：Adapter classes（桥接器）

```python
class SettingsModelManagerConfig:
    """Adapts AppSettings to the ModelManagerConfig protocol."""

    def __init__(self, settings: AppSettings):
        self._settings = settings

    @property
    def device(self) -> str:
        return self._settings.device

    @property
    def cache_maxsize(self) -> int:
        return self._settings.cache_maxsize
```

适配器提供了**间接性**：如果设置 schema 发生变化，只有适配器需要修改。`ModelManager` 本身不受影响。

## 在 main.py 中连接

```python
from app.config import get_settings
from app.config_adapters import SettingsModelManagerConfig
from app.model_manager import ModelManager

settings = get_settings()
config = SettingsModelManagerConfig(settings)
manager = ModelManager(config)
```

这种连接方式是显式且可追踪的。没有隐藏的全局状态，也没有魔法般的依赖注入框架。

## 使用假配置进行测试

```python
class FakeConfig:
    device = "cpu"
    cache_maxsize = 2
    cache_ttl = 60.0
    memory_threshold = 0.95

def test_model_manager_with_fake_config():
    manager = ModelManager(FakeConfig())
    assert manager.device == "cpu"
    assert manager.cache.maxsize == 2
```

协议驱动的设计意味着测试永远不需要 mock `os.environ` 或触碰 `.env` 文件。

## 延伸阅读

- [系统总览](/zh/architecture/overview)，了解配置在运行时拓扑中的位置
- [模型缓存](/zh/architecture/model-cache)，了解缓存参数如何被消费
