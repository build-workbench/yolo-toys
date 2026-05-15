---
layout: home

hero:
  name: "YOLO-Toys"
  text: "Multi-Model Vision Inference Platform"
  tagline: "Unified FastAPI + WebSocket interface for YOLO, DETR, OWL-ViT, Grounding DINO, and BLIP models"
  image:
    src: /images/logo.svg
    alt: YOLO-Toys Logo
  actions:
    - theme: brand
      text: Quick Start
      link: /en/getting-started/
    - theme: alt
      text: Academy
      link: /en/academy/
    - theme: alt
      text: GitHub
      link: https://github.com/LessUp/yolo-toys

features:
  - icon: 🚀
    title: Multi-Model Support
    details: "Run 8 model families in one service: YOLO, DETR, OWL-ViT, Grounding DINO, BLIP, SAM, RT-DETR, and more."
  - icon: ⚡
    title: Dual Protocol
    details: "REST for synchronous inference, WebSocket for real-time streaming. Same models, flexible access."
  - icon: 🏗️
    title: Handler Architecture
    details: "Strategy pattern for extensibility. Add custom models with minimal code changes."
  - icon: 📦
    title: Production Ready
    details: "Docker deployment, <50ms latency, TTL+LRU caching, FP16 inference, health checks."
---

## Quick Start

```bash
docker run -p 8000:8000 ghcr.io/lessup/yolo-toys:latest
```

Then open [http://localhost:8000](http://localhost:8000) for the API UI.

## Architecture Overview

```mermaid
graph TB
    subgraph Client["Client"]
        WEB[Web UI]
        CLI[CLI Tool]
        SDK[SDK]
    end

    subgraph API["API Layer"]
        REST[REST API]
        WS[WebSocket]
    end

    subgraph Core["Core"]
        MM[ModelManager]
        REG[HandlerRegistry]
        CACHE[ModelCache]
    end

    subgraph Handlers["Handlers"]
        YOLO[YOLOHandler]
        DETR[DETRHandler]
        BLIP[BLIPHandler]
    end

    Client --> API
    API --> MM
    MM --> REG --> Handlers
```
