---
layout: home
---

<WhitepaperLanding
  eyebrow="YOLO-Toys"
  chapter="架构白皮书"
  title="把异构视觉模型统一到一个运行时里，并像系统论文一样把它讲清楚。"
  abstract="YOLO-Toys 把 YOLOv8、DETR、OWL-ViT、Grounding DINO 与 BLIP 统一到一条 FastAPI 与 WebSocket 服务边界中。这个站点不是普通文档站，而是围绕架构图谱、设计推演、运行参考与研究背景展开的项目导读。"
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
    <span>Handler / Registry</span>
    <span>研究导向文档</span>
  </template>

  <template #figure>
    <FigureFrame
      title="系统论点"
      caption="YOLO-Toys 的核心目标，是在不抹平模型差异的前提下统一其服务边界。"
    >
      <div class="yt-home-figure-shell">
        <div class="yt-home-figure-step">
          <strong>客户端表面</strong>
          <span>HTTP、WebSocket、观测端点</span>
        </div>
        <div class="yt-home-figure-step">
          <strong>运行时核心</strong>
          <span>ModelManager、缓存策略、并发护栏</span>
        </div>
        <div class="yt-home-figure-step">
          <strong>执行适配层</strong>
          <span>YOLO、DETR、OWL-ViT、Grounding DINO、BLIP 处理器</span>
        </div>
      </div>
    </FigureFrame>
  </template>

  <template #tracks>
    <ReadingTracks
      :tracks="[
        {
          title: '面试官 / 审查者',
          summary: '先读架构图谱，再看竞品对比与参考文献，快速建立判断。',
          href: '/zh/architecture/'
        },
        {
          title: '集成者 / 运维者',
          summary: '先走导读，再看部署与 API 页面，明确系统落地方式。',
          href: '/zh/primer/'
        },
        {
          title: '贡献者 / 扩展者',
          summary: '先读学院文章，理解 handler 与 registry 的边界之后再改代码。',
          href: '/zh/academy/'
        }
      ]"
    />
  </template>
</WhitepaperLanding>
