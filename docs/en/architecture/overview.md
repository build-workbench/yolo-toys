# Architecture Overview

YOLO-Toys is easiest to understand as a **normalized serving runtime**. The goal is not to hide the fact that different vision models behave differently. The goal is to make those differences live behind explicit execution boundaries instead of leaking into every route, payload, and deployment concern.

<FigureFrame
  title="Figure 1. Runtime topology"
  caption="The service is deliberately layered so route handling, model resolution, execution, caching, and result shaping do not collapse into the same abstraction."
>
  <img src="/images/hero-architecture.svg" alt="YOLO-Toys runtime topology" />
</FigureFrame>

## Layer model

| Layer | Responsibility | Why it exists |
| --- | --- | --- |
| API surface | HTTP and WebSocket ingress | Keeps transport concerns separate from model logic |
| Runtime coordination | `ModelManager`, concurrency controls, cache policy | Centralizes lifecycle and resource decisions |
| Dispatch and metadata | `HandlerRegistry`, model registry entries | Makes model lookup deterministic and inspectable |
| Execution adapters | YOLO, DETR, OWL-ViT, Grounding DINO, BLIP handlers | Contains model-family-specific behavior |
| Result normalization | shared schemas and formatter helpers | Preserves a coherent public contract |

## The central architectural bet

The project makes one strong bet: **heterogeneous models can share a service boundary if their execution differences are pushed into handler adapters and their public outputs are normalized aggressively enough**.

That bet creates three wins:

1. API consumers do not need a different integration style per model family.
2. New model families can be added with limited surface churn.
3. Architectural trade-offs stay visible because the adapters remain explicit.

It also creates one cost:

- the runtime must own more translation work between upstream model semantics and downstream API semantics

## Why the manager layer is central

`ModelManager` is not a convenience wrapper. It is the runtime's control plane. It decides when models are loaded, when cached instances should be reused, and how inference requests move toward the right handler without route-level duplication.

## Why the registry matters

The registry is the project's **semantic index**. It does more than map IDs to handlers. It records model category, task type, metadata, and parameter expectations. That makes the service introspectable through `/models`, keeps dispatch deterministic, and gives the docs a single factual backbone.

## What to read next

- [Request Lifecycle](/en/architecture/request-flow) for the end-to-end inference path
- [Handler Pattern](/en/academy/handler-pattern) for the adapter boundary
- [Registry Pattern](/en/academy/registry-pattern) for model metadata and dispatch reasoning
