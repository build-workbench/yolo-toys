---
layout: home
---

<WhitepaperLanding
  eyebrow="YOLO-Toys"
  chapter="架构白皮书"
  title="把异构视觉模型统一到一个运行时里，并像系统论文一样把它讲清楚。"
  abstract="YOLO-Toys 把 YOLOv8、DETR、OWL-ViT、Grounding DINO 与 BLIP 统一到一条 FastAPI 与 WebSocket 服务边界中。这个站点把代码库当作技术工件来对待：架构图谱、设计推演、运行参考与研究背景——以系统白皮书的标准进行文档化。"
  primary-label="从导读开始"
  primary-href="/zh/primer/"
  secondary-label="进入架构图谱"
  secondary-href="/zh/architecture/"
  tertiary-label="查看 API"
  tertiary-href="/zh/api/"
  github-href="https://github.com/LessUp/yolo-toys"
>
  <template #signals>
    <span>5 个模型家族</span>
    <span>REST + WebSocket</span>
    <span>Handler / Registry 模式</span>
    <span>LRU + TTL 缓存</span>
  </template>

  <template #figure>
    <FigureFrame
      title="运行时架构"
      caption="YOLO-Toys 组织为规范化的服务运行时：传输层入口、中央控制平面、注册表支撑的分发调度，以及将异构执行逻辑局部化的模型家族适配层。"
    >
      <SvgRenderer src="/images/hero-architecture.svg" alt="YOLO-Toys 运行时拓扑" title="运行时拓扑" />
    </FigureFrame>
  </template>

  <template #stats>
    <div class="yt-section-label">运行时特征</div>
    <div class="yt-stat-grid">
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">&lt;5ms</span>
        <span class="yt-stat-card__label">热启动延迟</span>
        <span class="yt-stat-card__detail">YOLOv8n + GPU，缓存命中路径</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">5</span>
        <span class="yt-stat-card__label">模型家族</span>
        <span class="yt-stat-card__detail">YOLO · DETR · OWL-ViT · G-DINO · BLIP</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">142</span>
        <span class="yt-stat-card__label">请求/秒</span>
        <span class="yt-stat-card__detail">YOLOv8n 已缓存，20 并发用户</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">85%</span>
        <span class="yt-stat-card__label">内存阈值</span>
        <span class="yt-stat-card__detail">GPU 安全驱逐的 LRU 触发线</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">6</span>
        <span class="yt-stat-card__label">中间件层</span>
        <span class="yt-stat-card__detail">安全 → 指标 → 超时 → 限流 → 压缩 → CORS</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">1</span>
        <span class="yt-stat-card__label">服务边界</span>
        <span class="yt-stat-card__detail">所有模型家族统一在单个 FastAPI 运行时后</span>
      </div>
    </div>
  </template>

  <template #blueprint>
    <div class="yt-blueprint">
      <div class="yt-blueprint__header">
        <span class="yt-blueprint__title">架构蓝图</span>
      </div>
      <div class="yt-blueprint__layers">
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">API 表面</span>
          <span class="yt-blueprint__layer-desc">HTTP REST + WebSocket 入口——路由保持轻薄、传输专属、可替换</span>
          <span class="yt-blueprint__layer-tag">传输层</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">中间件栈</span>
          <span class="yt-blueprint__layer-desc">SecurityHeaders → Metrics → Timeout → RateLimit → GZip → CORS 按层序执行</span>
          <span class="yt-blueprint__layer-tag">横切关注点</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">运行时核心</span>
          <span class="yt-blueprint__layer-desc">ModelManager——缓存策略、并发护栏、生命周期所有权</span>
          <span class="yt-blueprint__layer-tag">控制平面</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">Handler 注册表</span>
          <span class="yt-blueprint__layer-desc">HandlerRegistry——类别推断、模型元数据、确定性分发</span>
          <span class="yt-blueprint__layer-tag">分发层</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">执行适配器</span>
          <span class="yt-blueprint__layer-desc">YOLO · DETR · OWL-ViT · Grounding DINO · BLIP handler——模型专属逻辑局部化</span>
          <span class="yt-blueprint__layer-tag">执行层</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">结果规范化</span>
          <span class="yt-blueprint__layer-desc">跨所有模型家族的稳定公开 schema——YOLO 与 DETR 使用相同 envelope</span>
          <span class="yt-blueprint__layer-tag">契约层</span>
        </div>
      </div>
    </div>
  </template>

  <template #tracks>
    <ReadingTracks
      :tracks="[
        {
          title: '运维者 / 集成者',
          summary: '先走导读以验证部署假设，再深入 API 表面与运维参考。',
          href: '/zh/primer/'
        },
        {
          title: '贡献者 / 扩展者',
          summary: '先读学院文章，理解 handler 与 registry 的边界之后再改代码。先理解「为什么」，再理解「怎么做」。',
          href: '/zh/academy/'
        },
        {
          title: '研究者 / 审阅者',
          summary: '从架构总览开始，再用研究章节获取学术背景、引用文献与对比分析。',
          href: '/zh/research/'
        }
      ]"
    />
  </template>
</WhitepaperLanding>
