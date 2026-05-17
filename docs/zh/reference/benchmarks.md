---
title: 性能基准测试
---

# 性能基准测试

这些基准测试确立了 YOLO-Toys 运行时的基线性能特征。它们不是与其他服务框架的竞争性对比；而是运维人员可用于调整缓存大小、超时值和并发限制的**内部基线**。

## 测试方法

所有基准测试均在以下环境下运行：

- **硬件**：Intel Core i7-12700H, 32 GB RAM, NVIDIA RTX 3060 Laptop GPU (6 GB VRAM)
- **软件**：Python 3.12, PyTorch 2.3.0, CUDA 12.1
- **图像**：640x480 BGR numpy 数组，随机噪声
- **预热**：测量前进行 3 次推理运行以稳定 GPU 时钟
- **指标**：墙上时钟时间（真实时间），单线程，使用 `time.perf_counter()` 测量

## 冷启动与热启动延迟

| 模型 | 冷启动 (CPU) | 冷启动 (CUDA) | 热启动 (CPU) | 热启动 (CUDA) |
|-------|-----------------|-------------------|-----------------|-------------------|
| yolov8n.pt | 0.45s | 0.12s | 0.018s | 0.004s |
| yolov8m.pt | 1.82s | 0.38s | 0.065s | 0.012s |
| facebook/detr-resnet-50 | 4.2s | 1.1s | 0.38s | 0.09s |
| google/owlvit-base-patch32 | 3.8s | 0.95s | 0.42s | 0.11s |
| Salesforce/blip-image-captioning-base | 2.1s | 0.55s | 0.28s | 0.07s |

### 关键发现

**冷启动惩罚是热启动延迟的 10–40 倍**。这正是 `ModelCache` 成为性能最关键组件的原因：每次缓存未命中耗时以秒计，而每次缓存命中仅需毫秒。

## 并发下的吞吐量

使用 `locust` 模拟（20 个并发用户，产生速率 5/秒）：

| 场景 | 请求/秒 | 平均延迟 | 95 分位延迟 |
|----------|-------------|-------------|---------------|
| 单模型 (yolov8n.pt)，已缓存 | 142 | 120ms | 180ms |
| 双模型轮换，均已缓存 | 118 | 145ms | 220ms |
| 每第 3 个请求缓存未命中 | 38 | 420ms | 1.2s |
| GPU 内存已满（OOM 压力） | 12 | 1.8s | 5.2s |

### 运维要点

当缓存命中率降至约 80% 以下时，系统会进入**延迟悬崖**，吞吐量随之崩塌。请监控 `/metrics` 端点的 `cache_size`，并在其接近 `cache_maxsize` 时设置告警。

## 内存占用

| 模型 | PyTorch 模型大小 | 峰值 VRAM（推理） | 缓存开销 |
|-------|-------------------|----------------------|----------------|
| yolov8n.pt | 6.2 MB | 180 MB | ~2 MB |
| yolov8m.pt | 49.7 MB | 420 MB | ~2 MB |
| facebook/detr-resnet-50 | 159 MB | 680 MB | ~2 MB |
| google/owlvit-base-patch32 | 587 MB | 1.1 GB | ~2 MB |
| Salesforce/blip-image-captioning-base | 990 MB | 1.6 GB | ~2 MB |

在 6 GB GPU 上使用默认 `cache_maxsize=3` 时：

- 3 个 BLIP 模型 = **OOM**（约 4.8 GB）
- 2 个 BLIP + 1 个 DETR = **OOM**（约 3.9 GB）
- 3 个 DETR = **正常**（约 2.0 GB）
- 1 个 BLIP + 1 个 DETR + 1 个 YOLO = **正常**（约 2.3 GB）

这正是 `memory_threshold=0.85` 至关重要的原因：它在 GPU 耗尽之前触发 LRU 驱逐。

## 在你自己的环境中进行基准测试

YOLO-Toys 包含一个 pytest-benchmark 测试套件：

```bash
cd /path/to/yolo-toys
pytest tests/benchmarks/ --benchmark-only
```

基准测试套件涵盖：

- 每模型家族的加载时间
- 每模型家族的推理延迟
- 缓存命中与未命中延迟
- 并发请求吞吐量

## 接下来阅读什么

- [模型缓存](/en/architecture/model-cache) 这些基准测试所验证的缓存策略
- [请求生命周期](/en/architecture/request-flow) 了解延迟在流水线中的分布
- [对比](/en/reference/comparisons) 了解这些数字与相邻服务系统的比较
