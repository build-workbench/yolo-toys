# Primer

The Primer is the shortest path from first contact to architectural confidence. Read this chapter if you need to understand what YOLO-Toys does, which model families it unifies, and where to dive next.

## What YOLO-Toys actually is

YOLO-Toys is a **multi-model vision serving runtime**. It puts several distinct model families behind one FastAPI and WebSocket surface so you can compare model behavior, integrate a demo backend quickly, or study a clean serving architecture for mixed computer-vision workloads.

## Surfaces to understand first

| Surface | Why it matters |
| --- | --- |
| `/infer` | Unified detection, segmentation, pose, and open-vocabulary inference |
| `/caption` and `/vqa` | Vision-language entry points powered by BLIP |
| `/ws` | Real-time frame streaming for lower-latency feedback loops |
| `/models` and `/labels` | Discovery surfaces for runtime introspection |
| `/metrics`, `/health`, `/system/*` | Operational observability and guardrails |

## Reading sequence

1. [Quickstart](/en/getting-started/quickstart) to see the shortest runnable path
2. [Installation](/en/getting-started/installation) if you want to develop locally
3. [Deployment Overview](/en/deployment/) for runtime packaging and environments
4. [Architecture Atlas](/en/architecture/) when you want the deeper design rationale

## Model families in scope

| Family | Representative models | Primary role |
| --- | --- | --- |
| YOLOv8 | `yolov8n.pt`, `yolov8n-seg.pt`, `yolov8n-pose.pt` | fast detection, segmentation, pose |
| DETR | `facebook/detr-resnet-50` | transformer-based detection |
| OWL-ViT / Grounding DINO | `google/owlvit-base-patch32` | open-vocabulary detection |
| BLIP | `Salesforce/blip-image-captioning-base` | captioning and VQA |

## What to read after this page

- Need the system map: go to [Architecture Atlas](/en/architecture/)
- Need design reasoning: go to [Academy](/en/academy/)
- Need endpoints and models: go to [Reference](/en/reference/)
- Need citations and adjacent systems: go to [Research](/en/research/)
