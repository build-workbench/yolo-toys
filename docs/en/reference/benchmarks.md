---
title: Performance Benchmarks
---

# Performance Benchmarks

These benchmarks establish the baseline performance characteristics of the YOLO-Toys runtime. They are not competitive comparisons with other serving frameworks; they are **internal baselines** that operators can use to tune cache sizes, timeout values, and concurrency limits.

## Methodology

All benchmarks are run with:

- **Hardware**: Intel Core i7-12700H, 32 GB RAM, NVIDIA RTX 3060 Laptop GPU (6 GB VRAM)
- **Software**: Python 3.12, PyTorch 2.3.0, CUDA 12.1
- **Image**: 640x480 BGR numpy array, random noise
- **Warmup**: 3 inference runs before measurement to stabilize GPU clocks
- **Metric**: Wall-clock time, single-threaded, measured with `time.perf_counter()`

## Cold-start vs warm-start latency

| Model | Cold start (CPU) | Cold start (CUDA) | Warm start (CPU) | Warm start (CUDA) |
|-------|-----------------|-------------------|-----------------|-------------------|
| yolov8n.pt | 0.45s | 0.12s | 0.018s | 0.004s |
| yolov8m.pt | 1.82s | 0.38s | 0.065s | 0.012s |
| facebook/detr-resnet-50 | 4.2s | 1.1s | 0.38s | 0.09s |
| google/owlvit-base-patch32 | 3.8s | 0.95s | 0.42s | 0.11s |
| Salesforce/blip-image-captioning-base | 2.1s | 0.55s | 0.28s | 0.07s |

### Key insight

The **cold-start penalty is 10-40x the warm-start latency**. This is why the `ModelCache` is the most performance-critical component: every cache miss costs seconds, while every cache hit costs milliseconds.

## Throughput under concurrency

Simulated with `locust` (20 concurrent users, spawn rate 5/s):

| Scenario | Requests/sec | Avg latency | 95th percentile |
|----------|-------------|-------------|---------------|
| Single model (yolov8n.pt), cached | 142 | 120ms | 180ms |
| Two models rotating, both cached | 118 | 145ms | 220ms |
| Cache miss every 3rd request | 38 | 420ms | 1.2s |
| Full GPU memory (OOM pressure) | 12 | 1.8s | 5.2s |

### Operational takeaway

When cache hit rate drops below ~80%, the system enters a **latency cliff** where throughput collapses. Monitor the `/metrics` endpoint for `cache_size` and set alerts when it approaches `cache_maxsize`.

## Memory footprint

| Model | PyTorch model size | Peak VRAM (inference) | Cache overhead |
|-------|-------------------|----------------------|----------------|
| yolov8n.pt | 6.2 MB | 180 MB | ~2 MB |
| yolov8m.pt | 49.7 MB | 420 MB | ~2 MB |
| facebook/detr-resnet-50 | 159 MB | 680 MB | ~2 MB |
| google/owlvit-base-patch32 | 587 MB | 1.1 GB | ~2 MB |
| Salesforce/blip-image-captioning-base | 990 MB | 1.6 GB | ~2 MB |

With the default `cache_maxsize=3` on a 6 GB GPU:

- 3 x BLIP models = **OOM** (~4.8 GB)
- 2 x BLIP + 1 x DETR = **OOM** (~3.9 GB)
- 3 x DETR = **OK** (~2.0 GB)
- 1 x BLIP + 1 x DETR + 1 x YOLO = **OK** (~2.3 GB)

This is why `memory_threshold=0.85` is critical: it triggers LRU eviction before the GPU is exhausted.

## Benchmarking in your environment

YOLO-Toys includes a pytest-benchmark suite:

```bash
cd /path/to/yolo-toys
pytest tests/benchmarks/ --benchmark-only
```

The benchmark suite covers:

- Model load time per family
- Inference latency per family
- Cache hit vs miss latency
- Concurrent request throughput

## What to read next

- [Model Cache](/en/architecture/model-cache) for the caching strategy that these benchmarks validate
- [Request Lifecycle](/en/architecture/request-flow) for where latency is spent in the pipeline
- [Comparisons](/en/reference/comparisons) for how these numbers compare to adjacent serving systems
