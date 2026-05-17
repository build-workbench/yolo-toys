---
layout: home
---

<WhitepaperLanding
  eyebrow="YOLO-Toys"
  chapter="Architecture Whitepaper"
  title="One runtime for heterogeneous vision models, documented like a systems paper."
  abstract="YOLO-Toys unifies YOLOv8, DETR, OWL-ViT, Grounding DINO, and BLIP behind a single FastAPI plus WebSocket service boundary. The site treats the repository as a technical artifact first: architecture atlas, design essays, operational references, and research context."
  primary-label="Start with the Primer"
  primary-href="/en/primer/"
  secondary-label="Open the Architecture Atlas"
  secondary-href="/en/architecture/"
  tertiary-label="Inspect the API Surface"
  tertiary-href="/en/api/"
  github-href="https://github.com/LessUp/yolo-toys"
>
  <template #signals>
    <span>5 model families</span>
    <span>REST + WebSocket</span>
    <span>Handler/Registry pattern</span>
    <span>Research-aware docs</span>
  </template>

  <template #figure>
    <FigureFrame
      title="System thesis"
      caption="YOLO-Toys is organized to normalize heterogeneous model families without flattening their differences."
    >
      <div class="yt-home-figure-shell">
        <div class="yt-home-figure-step">
          <strong>Client surfaces</strong>
          <span>HTTP, WebSocket, observability endpoints</span>
        </div>
        <div class="yt-home-figure-step">
          <strong>Runtime core</strong>
          <span>ModelManager, cache policy, concurrency guardrails</span>
        </div>
        <div class="yt-home-figure-step">
          <strong>Execution adapters</strong>
          <span>YOLO, DETR, OWL-ViT, Grounding DINO, BLIP handlers</span>
        </div>
      </div>
    </FigureFrame>
  </template>

  <template #tracks>
    <ReadingTracks
      :tracks="[
        {
          title: 'Integrator / Operator',
          summary: 'Start in the primer, validate deployment assumptions, then move into API and operations pages.',
          href: '/en/primer/'
        },
        {
          title: 'Contributor / Extender',
          summary: 'Read the academy essays to understand the handler and registry boundaries before touching code.',
          href: '/en/academy/'
        }
      ]"
    />
  </template>
</WhitepaperLanding>
