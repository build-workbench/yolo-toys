---
layout: home
---

<div class="home-header">
  <div class="home-header-left">
    <div class="home-logo">YT</div>
    <div>
      <span class="home-title">YOLO-Toys</span>
      <span class="home-subtitle">Vision Inference Service</span>
    </div>
  </div>
  <div class="home-nav">
    <a href="./getting-started/">Getting Started</a>
    <a href="https://github.com/LessUp/yolo-toys">GitHub</a>
    <a href="../zh/">中文</a>
  </div>
</div>

<div class="home-intro-row">
  <div class="home-intro">
    Multi-model vision inference service with unified FastAPI + WebSocket interface. Run YOLO, DETR, OWL-ViT, Grounding DINO, and BLIP models with a single service.
  </div>
  <div class="home-stats">
    <span><strong>Multi-model</strong> unified</span>
    <span><strong>REST</strong> + WebSocket</span>
    <span><strong>GPU</strong> accelerated</span>
  </div>
</div>

## Features

<div class="feature-map">
  <div class="feature-card">
    <div class="feature-card-title">🚀 Multi-Model Support</div>
    <div class="feature-card-desc">
      One service for YOLOv8, DETR, OWL-ViT, Grounding DINO, and BLIP models.
    </div>
    <div class="feature-tags">
      <a href="./reference/models" class="feature-tag">Model List</a>
      <a href="./guides/adding-models" class="feature-tag">Add Models</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">🔌 REST API</div>
    <div class="feature-card-desc">
      Simple HTTP endpoints for single-image detection with JSON responses.
    </div>
    <div class="feature-tags">
      <a href="./api/rest-api" class="feature-tag">REST Docs</a>
      <a href="./getting-started/quickstart" class="feature-tag">Quick Start</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">⚡ WebSocket Streaming</div>
    <div class="feature-card-desc">
      Real-time detection via WebSocket for video streams and continuous inference.
    </div>
    <div class="feature-tags">
      <a href="./api/websocket" class="feature-tag">WebSocket Docs</a>
      <a href="./api/" class="feature-tag">API Overview</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">🏗️ Handler Architecture</div>
    <div class="feature-card-desc">
      Model isolation with handler pattern. Easy to extend with new models.
    </div>
    <div class="feature-tags">
      <a href="./architecture/handlers" class="feature-tag">Handler Guide</a>
      <a href="./architecture/" class="feature-tag">Architecture</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">🎮 GPU Acceleration</div>
    <div class="feature-card-desc">
      NVIDIA CUDA, Apple MPS, and CPU backends. Auto-detect and optimize.
    </div>
    <div class="feature-tags">
      <a href="./deployment/environments" class="feature-tag">Environments</a>
      <a href="./deployment/docker" class="feature-tag">Docker</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">📦 Production Ready</div>
    <div class="feature-card-desc">
      Docker images, clean CLI, &lt;50ms latency. Ready for deployment.
    </div>
    <div class="feature-tags">
      <a href="./deployment/" class="feature-tag">Deployment</a>
      <a href="./getting-started/installation" class="feature-tag">Installation</a>
    </div>
  </div>
</div>

<div class="quick-start">
  <div class="quick-start-title">Quick Start</div>
  <div class="quick-start-content">
    <div class="command-block">
      <code>docker run -p 8000:8000 ghcr.io/lessup/yolo-toys:latest</code>
    </div>
    Then open <code>http://localhost:8000/docs</code> for the API UI.
  </div>
</div>
