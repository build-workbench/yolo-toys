# 架构总览

理解 YOLO-Toys 最好的方式，是把它看成一个 **归一化的模型服务运行时**。系统的目标不是掩盖不同视觉模型之间的差异，而是把这些差异约束在明确的执行边界之内，而不是泄漏到每条路由、每种请求参数和每套部署逻辑里。

<FigureFrame
  title="图 1. 运行时拓扑"
  caption="服务被刻意分层，避免路由处理、模型解析、执行、缓存与结果整形混在同一个抽象里。"
>
  <img src="/images/hero-architecture.svg" alt="YOLO-Toys 运行时拓扑" />
</FigureFrame>

## 分层模型

| 层 | 职责 | 为什么需要它 |
| --- | --- | --- |
| API 表面 | HTTP 与 WebSocket 入口 | 把传输层问题与模型执行分开 |
| 运行时协调层 | `ModelManager`、并发控制、缓存策略 | 把生命周期与资源决策集中起来 |
| 分发与元数据层 | `HandlerRegistry`、模型注册表 | 让模型查找可预测、可审计 |
| 执行适配层 | YOLO、DETR、OWL-ViT、Grounding DINO、BLIP handlers | 容纳模型家族特有行为 |
| 结果归一化层 | 共享 schema 与 formatter helper | 维持统一的公共契约 |

## 这套架构押注了什么

项目做了一个强烈的架构押注：**只要把执行差异推入 handler 适配层，并且对外结果做足够明确的归一化，异构模型就可以共享同一条服务边界**。

这个押注带来三点收益：

1. API 消费方不需要按模型家族切换集成方式
2. 新模型家族可以在较小的表面扰动下被接入
3. 架构权衡保持可见，因为适配边界没有被隐藏

同时也带来一个代价：

- 运行时必须承担更多“上游模型语义 -> 下游 API 语义”的翻译工作

## 为什么 manager 层是核心

`ModelManager` 不是一个顺手包了一层的 helper，它是运行时的控制平面。它决定模型何时加载、何时复用缓存实例，以及请求如何在不复制路由逻辑的前提下到达正确的 handler。

## 为什么 registry 很重要

Registry 是项目的 **语义索引**。它不只是把模型 ID 映射到 handler，还记录模型类别、任务类型、元数据和参数期望。这使 `/models` 具备可解释性，也让分发与文档都能共享同一份事实来源。

## 下一步阅读

- 去看 [请求流程](/zh/architecture/request-flow) 追完整条推理路径
- 去看 [Handler 模式](/zh/academy/handler-pattern) 理解适配边界
- 去看 [Registry 模式](/zh/academy/registry-pattern) 理解元数据与分发关系
