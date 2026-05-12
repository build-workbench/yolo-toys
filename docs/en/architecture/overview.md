# Architecture Overview

High-level system design and component interactions.

## System Components

### 1. API Layer

The API layer provides two interfaces:

- **REST API** — HTTP endpoints for single-image inference
- **WebSocket** — Real-time streaming for video analysis

### 2. Handler Manager

Responsible for:
- Model lifecycle management
- Dynamic model loading/unloading
- Resource allocation

### 3. Handlers

Each model type has its own handler:
- Encapsulates model-specific logic
- Implements standard interface
- Manages model resources

## Request Flow

```
1. Client Request
        │
        ▼
2. API Router
        │
        ▼
3. Handler Manager
        │
        ▼
4. Model Handler
        │
        ▼
5. Inference Engine
        │
        ▼
6. Response
```

## Design Principles

- **Single Responsibility** — Each handler does one thing well
- **Open/Closed** — Add models without modifying existing code
- **Dependency Inversion** — Depend on handler abstractions
