---
layout: home

hero:
  name: "YOLO-Toys"
  text: "多模型视觉推理平台"
  tagline: "统一的 FastAPI + WebSocket 接口，支持 YOLO、DETR、OWL-ViT、Grounding DINO 和 BLIP 模型"
  image:
    src: /images/logo.svg
    alt: YOLO-Toys Logo
  actions:
    - theme: brand
      text: 快速开始
      link: /zh/getting-started/
    - theme: alt
      text: 深度学院
      link: /zh/academy/
    - theme: alt
      text: GitHub
      link: https://github.com/LessUp/yolo-toys

features:
  - icon: 🚀
    title: 多模型支持
    details: "一个服务运行 8 种模型家族：YOLO、DETR、OWL-ViT、Grounding DINO、BLIP、SAM、RT-DETR 等。"
  - icon: ⚡
    title: 双协议支持
    details: "REST 同步推理，WebSocket 实时流。同一模型，灵活访问。"
  - icon: 🏗️
    title: Handler 架构
    details: "策略模式实现可扩展性。最小代码变更添加自定义模型。"
  - icon: 📦
    title: 生产就绪
    details: "Docker 部署，<50ms 延迟，TTL+LRU 缓存，FP16 推理，健康检查。"
---

## 快速开始

```bash
docker run -p 8000:8000 ghcr.io/lessup/yolo-toys:latest
```

然后访问 [http://localhost:8000](http://localhost:8000) 查看 API 界面。

## 架构概览

```mermaid
graph TB
    subgraph Client["客户端"]
        WEB[Web UI]
        CLI[CLI 工具]
        SDK[SDK]
    end

    subgraph API["API 层"]
        REST[REST API]
        WS[WebSocket]
    end

    subgraph Core["核心层"]
        MM[ModelManager]
        REG[HandlerRegistry]
        CACHE[ModelCache]
    end

    subgraph Handlers["处理器"]
        YOLO[YOLOHandler]
        DETR[DETRHandler]
        BLIP[BLIPHandler]
    end

    Client --> API
    API --> MM
    MM --> REG --> Handlers
```
