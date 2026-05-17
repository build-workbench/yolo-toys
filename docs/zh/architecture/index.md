# 架构图谱

<div class="yt-chapter-intro">
  <p class="yt-chapter-intro__lead">
    架构图谱章节回答的不是“有哪些文件”，而是“这个运行时为什么被组织成这样”。你会看到为什么路由层保持轻薄、为什么模型分发集中在 manager / registry，以及异构模型如何共享同一条服务契约。
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
</div>

## 本章要回答的问题

- 为什么不按模型家族拆成多套接口？
- 为什么模型解析要经过 registry？
- 结果归一化发生在哪一层，代价是什么？
- 系统如何在保持扩展性的同时不失去可理解性？

## 建议阅读顺序

1. 先读 [系统总览](/zh/architecture/overview)
2. 再读 [请求流程](/zh/architecture/request-flow)
3. 最后顺着 ADR 看关键设计取舍
