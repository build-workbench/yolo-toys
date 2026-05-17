# Config Injection

YOLO-Toys uses a **layered configuration system** that separates declarative settings (what the operator wants) from programmatic configuration (what the runtime needs). This separation makes the system testable, environment-aware, and safe to evolve.

## Design philosophy

The configuration stack follows three principles:

1. **Pydantic-first**: all settings are validated schemas, not raw dictionaries
2. **Environment-aware**: `.env` files, environment variables, and programmatic overrides coexist cleanly
3. **Protocol-driven**: internal modules depend on protocols (interfaces), not concrete settings classes

## Settings hierarchy

Configuration is resolved in the following priority order (highest to lowest):

```
1. Programmatic arguments passed at initialization
2. Environment variables (e.g., YOLOTOYS_DEVICE=cuda:0)
3. .env file in the working directory
4. Default values defined in Pydantic model
```

## The three config layers

### Layer 1: AppSettings (declarative)

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

This is the **operator-facing** layer. An operator changes behavior by setting environment variables or editing `.env`.

### Layer 2: Protocols (contracts)

```python
class ModelManagerConfig(Protocol):
    device: str
    cache_maxsize: int
    cache_ttl: float
    memory_threshold: float
```

Protocols define **what a component needs**, not where the values come from. This is the key to testability: unit tests can pass fake config objects without touching the real settings infrastructure.

### Layer 3: Adapter classes (bridges)

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

Adapters provide **indirection**: if the settings schema changes, only the adapter needs to change. The `ModelManager` remains untouched.

## Wiring in main.py

```python
from app.config import get_settings
from app.config_adapters import SettingsModelManagerConfig
from app.model_manager import ModelManager

settings = get_settings()
config = SettingsModelManagerConfig(settings)
manager = ModelManager(config)
```

This wiring is explicit and traceable. No hidden global state, no magic dependency injection framework.

## Testing with fake config

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

The protocol-driven design means tests never need to mock `os.environ` or touch `.env` files.

## What to read next

- [System Overview](/en/architecture/overview) for where configuration fits in the runtime topology
- [Model Cache](/en/architecture/model-cache) for how cache parameters are consumed
