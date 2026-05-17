# 架构图谱

<div class="yt-chapter-intro">
  <p class="yt-chapter-intro__lead">
    架构图谱章节回答的不是"有哪些文件"，而是"这个运行时为什么被组织成这样"。你会看到为什么路由层保持轻薄、为什么模型分发集中在 manager / registry，以及异构模型如何共享同一条服务契约。
  </p>
  <div class="yt-chapter-callout">
    <strong>适合在这里进入的读者：</strong>
    想快速看懂系统骨架、请求执行路径，以及扩展边界该落在哪里的人。
  </div>
</div>

<div class="yt-chapter-grid">
  <a class="yt-chapter-card" href="/zh/architecture/overview">
    <strong>系统总览</strong>
    <span>把服务看成分层运行时，而不是若干零散接口。</span>
  </a>
  <a class="yt-chapter-card" href="/zh/architecture/request-flow">
    <strong>请求生命周期</strong>
    <span>顺着一次请求走完整条链路：入口、缓存、分发、执行、结果整形。</span>
  </a>
  <a class="yt-chapter-card" href="/zh/architecture/handlers">
    <strong>执行边界</strong>
    <span>理解模型特定逻辑如何被约束在 handler 内部。</span>
  </a>
  <a class="yt-chapter-card" href="/zh/architecture/middleware-stack">
    <strong>中间件栈</strong>
    <span>安全、指标、超时、限流、压缩、跨域，按层次排序。</span>
  </a>
  <a class="yt-chapter-card" href="/zh/architecture/config-injection">
    <strong>配置注入</strong>
    <span>Pydantic 设置如何通过适配器类流入运行时。</span>
  </a>
  <a class="yt-chapter-card" href="/zh/architecture/model-cache">
    <strong>模型缓存</strong>
    <span>LRU + TTL 混合缓存，带内存压力驱逐和线程安全。</span>
  </a>
</div>

## 本章要回答的问题

- 为什么不按模型家族拆成多套接口？
- 为什么模型解析要经过 registry？
- 结果归一化发生在哪一层，代价是什么？
- 系统如何在保持扩展性的同时不失去可理解性？
- 中间件栈的排序如何反映生产关切？
- 为什么缓存是运营感知的，而不只是基于时间？

## 建议阅读顺序

1. 先读 [系统总览](/zh/architecture/overview)
2. 再读 [请求流程](/zh/architecture/request-flow)
3. 读 [处理器体系](/zh/architecture/handlers) 了解执行边界
4. 读 [中间件栈](/zh/architecture/middleware-stack) 了解运营层
5. 读 [配置注入](/zh/architecture/config-injection) 了解设置流转
6. 读 [模型缓存](/zh/architecture/model-cache) 了解缓存策略
7. 最后顺着 ADR 看关键设计取舍
