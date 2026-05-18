---
layout: home
---

<WhitepaperLanding
  eyebrow="YOLO-Toys"
  chapter="Architecture Whitepaper"
  title="One runtime for heterogeneous vision models, documented like a systems paper."
  abstract="YOLO-Toys unifies YOLOv8, DETR, OWL-ViT, Grounding DINO, and BLIP behind a single FastAPI plus WebSocket service boundary. This site treats the repository as a technical artifact: architecture atlas, design essays, operational references, and research context — documented to the standard of a systems whitepaper."
  primary-label="Start with the Primer"
  primary-href="/en/primer/"
  secondary-label="Architecture Atlas"
  secondary-href="/en/architecture/"
  tertiary-label="API Reference"
  tertiary-href="/en/api/"
  github-href="https://github.com/LessUp/yolo-toys"
>
  <template #signals>
    <span>5 model families</span>
    <span>REST + WebSocket</span>
    <span>Handler / Registry pattern</span>
    <span>LRU + TTL cache</span>
  </template>

  <template #figure>
    <FigureFrame
      title="Runtime architecture"
      caption="YOLO-Toys is organized as a normalized serving runtime: transport-specific ingress, a central control plane, registry-backed dispatch, and model-family adapters that keep heterogeneous execution localized."
    >
      <SvgRenderer src="/images/hero-architecture.svg" alt="YOLO-Toys runtime topology" title="Runtime Topology" />
    </FigureFrame>
  </template>

  <template #stats>
    <div class="yt-section-label">Runtime characteristics</div>
    <div class="yt-stat-grid">
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">&lt;5ms</span>
        <span class="yt-stat-card__label">Warm latency</span>
        <span class="yt-stat-card__detail">YOLOv8n on GPU, cache hit path</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">5</span>
        <span class="yt-stat-card__label">Model families</span>
        <span class="yt-stat-card__detail">YOLO · DETR · OWL-ViT · G-DINO · BLIP</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">142</span>
        <span class="yt-stat-card__label">Requests / sec</span>
        <span class="yt-stat-card__detail">YOLOv8n cached, 20 concurrent users</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">85%</span>
        <span class="yt-stat-card__label">Memory threshold</span>
        <span class="yt-stat-card__detail">LRU eviction trigger for GPU safety</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">6</span>
        <span class="yt-stat-card__label">Middleware layers</span>
        <span class="yt-stat-card__detail">Security → Metrics → Timeout → Rate → GZip → CORS</span>
      </div>
      <div class="yt-stat-card">
        <span class="yt-stat-card__value">1</span>
        <span class="yt-stat-card__label">Service boundary</span>
        <span class="yt-stat-card__detail">All model families behind one FastAPI runtime</span>
      </div>
    </div>
  </template>

  <template #blueprint>
    <div class="yt-blueprint">
      <div class="yt-blueprint__header">
        <span class="yt-blueprint__title">Architecture blueprint</span>
      </div>
      <div class="yt-blueprint__layers">
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">API surface</span>
          <span class="yt-blueprint__layer-desc">HTTP REST + WebSocket ingress — routes stay thin, transport-specific, and replaceable</span>
          <span class="yt-blueprint__layer-tag">Transport</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">Middleware stack</span>
          <span class="yt-blueprint__layer-desc">SecurityHeaders → Metrics → Timeout → RateLimit → GZip → CORS in layered order</span>
          <span class="yt-blueprint__layer-tag">Cross-cutting</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">Runtime core</span>
          <span class="yt-blueprint__layer-desc">ModelManager — cache policy, concurrency guardrails, lifecycle ownership</span>
          <span class="yt-blueprint__layer-tag">Control plane</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">Handler registry</span>
          <span class="yt-blueprint__layer-desc">HandlerRegistry — category inference, model metadata, deterministic dispatch</span>
          <span class="yt-blueprint__layer-tag">Dispatch</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">Execution adapters</span>
          <span class="yt-blueprint__layer-desc">YOLO · DETR · OWL-ViT · Grounding DINO · BLIP handlers — model-specific logic localized</span>
          <span class="yt-blueprint__layer-tag">Execution</span>
        </div>
        <div class="yt-blueprint__layer">
          <span class="yt-blueprint__layer-name">Result normalization</span>
          <span class="yt-blueprint__layer-desc">Stable public schema across all model families — same envelope for YOLO and DETR</span>
          <span class="yt-blueprint__layer-tag">Contract</span>
        </div>
      </div>
    </div>
  </template>

  <template #tracks>
    <ReadingTracks
      :tracks="[
        {
          title: 'Operator / Integrator',
          summary: 'Start in the primer to validate deployment assumptions, then move through API surfaces and operational references.',
          href: '/en/primer/'
        },
        {
          title: 'Contributor / Extender',
          summary: 'Read the academy essays to understand handler and registry boundaries before writing code. Understand the why before the how.',
          href: '/en/academy/'
        },
        {
          title: 'Researcher / Reviewer',
          summary: 'Start at the architecture overview, then use the research chapter for academic context, citations, and comparative analysis.',
          href: '/en/research/'
        }
      ]"
    />
  </template>
</WhitepaperLanding>
