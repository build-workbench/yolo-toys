# Research

This chapter frames YOLO-Toys as more than a runtime. It collects the technical lineage behind the project, compares adjacent serving systems, and records the reasoning that makes the codebase legible to advanced readers.

## Research surfaces

| Surface | What it contributes |
| --- | --- |
| [Academic Citations](/en/citations) | Canonical bibliography for the supported model families and frameworks |
| [Comparisons](/en/reference/comparisons) | Trade-off analysis versus Triton, TorchServe, BentoML, and custom FastAPI stacks |
| [Architecture Atlas](/en/architecture/) | Runtime-level system model and execution-path explanations |
| [Academy](/en/academy/) | Long-form essays on patterns, trade-offs, and extensibility decisions |

## Why this chapter exists

Most OSS model-serving repositories stop at setup instructions. YOLO-Toys is more interesting when treated as a **teaching artifact**: a compact example of how to normalize heterogeneous vision models behind one service boundary without turning the runtime into an opaque monolith.

## Suggested reading path

1. Read the [Architecture Atlas](/en/architecture/) for the system shape
2. Use [Comparisons](/en/reference/comparisons) to situate the project among adjacent serving options
3. Use [Academic Citations](/en/citations) when you need the upstream technical lineage
4. Finish in [Academy](/en/academy/) for pattern-level reasoning
