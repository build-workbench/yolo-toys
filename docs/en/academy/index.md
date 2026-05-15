---
title: Academy - Deep Learning Patterns
---

# YOLO-Toys Academy

Welcome to YOLO-Toys Academy, a curated collection of in-depth technical explorations into the architectural patterns that power our multi-model vision inference platform.

## Purpose

This academy module serves as a knowledge repository for developers who want to understand the "why" behind our design decisions. Each article goes beyond API documentation to explore the theoretical foundations, trade-offs, and practical implementation details of our core patterns.

## What You'll Learn

### Design Patterns

| Pattern | Description | Article |
|---------|-------------|---------|
| **Handler Pattern** | Strategy pattern for unified multi-model inference | [Deep Dive →](/en/academy/handler-pattern) |
| **Registry Pattern** | Centralized metadata management and model discovery | [Deep Dive →](/en/academy/registry-pattern) |
| **Caching Strategy** | TTL + LRU hybrid eviction with memory pressure awareness | [Deep Dive →](/en/academy/caching-strategy) |
| **OpenSpec System** | Gherkin-based specification for behavioral contracts | [Deep Dive →](/en/academy/openspec-system) |

## Learning Path

We recommend reading these articles in the following order:

```
┌─────────────────────────────────────────────────────────────┐
│                    Learning Pathway                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. Handler Pattern ──▶ Core abstraction layer             │
│          │                                                   │
│          ▼                                                   │
│   2. Registry Pattern ──▶ Model discovery & routing         │
│          │                                                   │
│          ▼                                                   │
│   3. Caching Strategy ──▶ Performance optimization          │
│          │                                                   │
│          ▼                                                   │
│   4. OpenSpec System ──▶ Behavioral specification           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Target Audience

- **Backend Engineers** looking to implement similar multi-model systems
- **ML Engineers** interested in production deployment patterns
- **Software Architects** evaluating design trade-offs
- **Contributors** who want to extend YOLO-Toys with new models

## Article Standards

Each academy article follows a consistent structure:

1. **Problem Statement** - What challenge are we solving?
2. **Theoretical Foundation** - The pattern in software design literature
3. **Implementation Deep Dive** - Code-level analysis with diagrams
4. **Trade-offs** - What we gained and what we sacrificed
5. **Extension Guide** - How to customize or extend the pattern

## Quick Reference

### Model Categories

| Category | Task | Handler Class |
|----------|------|---------------|
| `yolo_detect` | Object Detection | `YOLOHandler` |
| `yolo_segment` | Instance Segmentation | `YOLOHandler` |
| `yolo_pose` | Pose Estimation | `YOLOHandler` |
| `hf_detr` | Detection (Transformer) | `DETRHandler` |
| `hf_owlvit` | Open-Vocabulary Detection | `OWLViTHandler` |
| `hf_grounding_dino` | Grounded Detection | `GroundingDINOHandler` |
| `multimodal_caption` | Image Captioning | `BLIPCaptionHandler` |
| `multimodal_vqa` | Visual Question Answering | `BLIPVQAHandler` |

### Core Abstractions

```python
# The three pillars of YOLO-Toys architecture
BaseHandler      # Strategy interface for model inference
HandlerRegistry  # Central dispatch for model resolution
ModelManager     # Facade with caching and lifecycle management
```

## Contributing

Found an error or want to add an article? See our [Contributing Guide](/en/community/contributing) for details on submitting improvements to the academy.
