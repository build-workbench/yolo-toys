# Request Lifecycle

This page follows one inference request through the runtime. The lifecycle matters because the quality of the public API depends on where the system translates, caches, validates, and formats.

<FigureFrame
  title="Figure 2. End-to-end lifecycle"
  caption="Requests enter through transport-specific surfaces but converge on a single coordination path before model-specific execution begins."
>
  <img src="/images/request-lifecycle.svg" alt="YOLO-Toys request lifecycle" />
</FigureFrame>

## The path, step by step

1. **Ingress**: the request enters through HTTP or WebSocket.
2. **Validation**: parameters, files, and model identifiers are checked before execution starts.
3. **Coordination**: `ModelManager` selects or reuses the model instance and resolves the handler.
4. **Execution**: the selected handler runs model-family-specific inference.
5. **Normalization**: raw outputs are shaped into stable response contracts.
6. **Emission**: the runtime returns JSON or streamed frame-level payloads.

## Why normalization sits after execution

Upstream models disagree on output shape, label semantics, confidence behavior, and auxiliary artifacts. If route handlers tried to normalize those differences directly, the transport layer would become the place where model semantics accumulate. YOLO-Toys instead keeps the route surface thin and lets handlers plus formatter helpers perform the translation.

## Cache and concurrency interactions

The lifecycle is not just functional, it is operational. A request path can trigger:

- a cache hit and immediate reuse of a warm model
- a lazy model load on first use
- waiting behind concurrency limits when the runtime is already saturated

Those interactions are part of the user-visible behavior because they shape latency, warm-up cost, and resource pressure.

## Failure surfaces

Common failures cluster at four points:

- invalid or oversized inputs
- unknown model identifiers
- runtime model-loading failures
- downstream inference errors inside handlers

The value of the current architecture is that each failure type has a natural boundary where it can be surfaced cleanly.
