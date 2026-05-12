---
layout: home
---

<div class="home-header">
  <div class="home-header-left">
    <div class="home-logo">YT</div>
    <div>
      <span class="home-title">YOLO-Toys</span>
      <span class="home-subtitle">视觉推理服务</span>
    </div>
  </div>
  <div class="home-nav">
    <a href="./getting-started/">入门指南</a>
    <a href="https://github.com/LessUp/yolo-toys">GitHub</a>
    <a href="../en/">English</a>
  </div>
</div>

<div class="home-intro-row">
  <div class="home-intro">
    多模型视觉推理服务，统一的 FastAPI + WebSocket 接口。一个服务运行 YOLO、DETR、OWL-ViT、Grounding DINO 和 BLIP 模型。
  </div>
  <div class="home-stats">
    <span><strong>多模型</strong>统一</span>
    <span><strong>REST</strong> + WebSocket</span>
    <span><strong>GPU</strong>加速</span>
  </div>
</div>

## 功能特性

<div class="feature-map">
  <div class="feature-card">
    <div class="feature-card-title">🚀 多模型支持</div>
    <div class="feature-card-desc">
      一个服务支持 YOLOv8、DETR、OWL-ViT、Grounding DINO 和 BLIP 模型。
    </div>
    <div class="feature-tags">
      <a href="./reference/models" class="feature-tag">模型列表</a>
      <a href="./guides/adding-models" class="feature-tag">添加模型</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">🔌 REST API</div>
    <div class="feature-card-desc">
      简单的 HTTP 端点，单张图片检测返回 JSON 响应。
    </div>
    <div class="feature-tags">
      <a href="./api/rest-api" class="feature-tag">REST 文档</a>
      <a href="./getting-started/quickstart" class="feature-tag">快速开始</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">⚡ WebSocket 流式</div>
    <div class="feature-card-desc">
      通过 WebSocket 实现实时检测，支持视频流和持续推理。
    </div>
    <div class="feature-tags">
      <a href="./api/websocket" class="feature-tag">WebSocket 文档</a>
      <a href="./api/" class="feature-tag">API 概览</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">🏗️ Handler 架构</div>
    <div class="feature-card-desc">
      模型隔离的 Handler 模式，易于扩展新模型。
    </div>
    <div class="feature-tags">
      <a href="./architecture/handlers" class="feature-tag">Handler 指南</a>
      <a href="./architecture/" class="feature-tag">架构设计</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">🎮 GPU 加速</div>
    <div class="feature-card-desc">
      支持 NVIDIA CUDA、Apple MPS 和 CPU 后端，自动检测优化。
    </div>
    <div class="feature-tags">
      <a href="./deployment/environments" class="feature-tag">环境配置</a>
      <a href="./deployment/docker" class="feature-tag">Docker</a>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-card-title">📦 生产就绪</div>
    <div class="feature-card-desc">
      Docker 镜像、简洁 CLI、&lt;50ms 延迟，可直接部署。
    </div>
    <div class="feature-tags">
      <a href="./deployment/" class="feature-tag">部署指南</a>
      <a href="./getting-started/installation" class="feature-tag">安装说明</a>
    </div>
  </div>
</div>

<div class="quick-start">
  <div class="quick-start-title">快速开始</div>
  <div class="quick-start-content">
    <div class="command-block">
      <code>docker run -p 8000:8000 ghcr.io/lessup/yolo-toys:latest</code>
    </div>
    然后访问 <code>http://localhost:8000/docs</code> 查看 API 界面。
  </div>
</div>
