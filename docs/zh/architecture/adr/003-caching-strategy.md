---
title: ADR-003 - TTL + LRU 混合缓存
---

# ADR-003：TTL + LRU 混合缓存

| 状态 | 日期 | 决策者 |
|------|------|--------|
| 已采纳 | 2024-01-20 | 架构团队 |

## 背景

模型加载代价高昂：
- YOLO 模型：100ms - 2s
- HuggingFace 模型：1s - 10s（网络 + 反序列化）
- GPU 内存：有限，模型占用 10MB - 500MB

我们需要一个缓存策略：
1. 避免重复加载代价
2. 防止内存耗尽
3. 处理不同的模型大小
4. 支持并发访问
5. 提供可观测性

## 决策

我们实现 **TTL + LRU 混合缓存**：
- TTLCache 基类用于基于时间的到期
- 内存超过阈值时 LRU 驱逐
- 用锁实现线程安全访问
- 内存压力监控

```python
class ModelCache(TTLCache):
    def __init__(self, maxsize, ttl, memory_threshold=0.85):
        super().__init__(maxsize=maxsize, ttl=ttl)
        self._access_times: dict[str, float] = {}
        self._lock = threading.Lock()
        self._memory_threshold = memory_threshold

    def __setitem__(self, key, value):
        with self._lock:
            if (len(self) >= self.maxsize or
                get_memory_usage() > self._memory_threshold):
                self._evict_lru_unsafe()
            super().__setitem__(key, value)
```

## 考虑的替代方案

### 替代方案 1：无缓存

每次请求都加载模型

**缺点**：高延迟（1-10s 每请求），浪费 CPU

### 替代方案 2：无界缓存

永远缓存所有加载的模型

**缺点**：内存无限增长（OOM 风险）

### 替代方案 3：仅 TTL

只用 TTL 无大小/内存限制

**缺点**：TTL 到期前内存可能飙升，热门模型每次 TTL 周期都重载

### 替代方案 4：仅 LRU

只用 LRU 无 TTL

**缺点**：热门模型永不刷新，不考虑内存压力

## 后果

### 正面

1. **响应速度**：缓存模型即时返回
2. **内存安全**：驱逐防止 OOM
3. **新鲜度**：TTL 确保定期刷新
4. **线程安全**：并发访问安全
5. **可配置**：环境变量调节行为

### 负面

1. **锁开销**：高并发下的竞争
2. **驱逐暂停**：GC/CUDA 清理期间的暂停
3. **配置复杂性**：三个参数需要调优

### 缓解措施

- **锁开销**：Python GIL 下最小
- **驱逐暂停**：不频繁，延迟可接受
- **配置复杂性**：合理默认值（maxsize=10, ttl=3600, threshold=0.85）

## 参考文献

- [cachetools.TTLCache](https://cachetools.readthedocs.io/en/stable/#cachetools.TTLCache)
- [缓存算法 - Wikipedia](https://en.wikipedia.org/wiki/Cache_replacement_policies)
