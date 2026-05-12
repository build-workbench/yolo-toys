# Architecture

Understanding YOLO-Toys system design and components.

## Overview

YOLO-Toys uses a modular handler-based architecture that enables:

- **Model Isolation** — Each model runs in its own handler
- **Easy Extension** — Add new models by implementing the handler interface
- **Unified API** — Single interface for all model types

## Core Components

| Component | Description |
|-----------|-------------|
| [Overview](./overview) | High-level system architecture |
| [Handlers](./handlers) | Handler design pattern and implementation |

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│                 API Layer                    │
│         (REST + WebSocket Endpoints)         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│              Handler Manager                 │
│     (Model Loading & Lifecycle Mgmt)         │
└──────────────────┬──────────────────────────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  YOLO    │ │   DETR   │ │ OWL-ViT  │
│ Handler  │ │ Handler  │ │ Handler  │
└──────────┘ └──────────┘ └──────────┘
```
