# Research

This chapter frames YOLO-Toys as more than a runtime. It collects the technical lineage behind the project, compares adjacent serving systems, and records the reasoning that makes the codebase legible to advanced readers.

## Research surfaces

| Surface | What it contributes |
| --- | --- |
| [Academic Citations](/en/citations) | Canonical bibliography for the supported model families and frameworks |
| [Comparisons](/en/reference/comparisons) | Trade-off analysis versus Triton, TorchServe, BentoML, and custom FastAPI stacks |
| [Evolution](/en/research/evolution) | Architectural history: from flat endpoints to handler boundaries, from naive caching to operational awareness |
| [Architecture Atlas](/en/architecture/) | Runtime-level system model and execution-path explanations |
| [Academy](/en/academy/) | Long-form essays on patterns, trade-offs, and extensibility decisions |

## Why this chapter exists

Most OSS model-serving repositories stop at setup instructions. YOLO-Toys is more interesting when treated as a **teaching artifact**: a compact example of how to normalize heterogeneous vision models behind one service boundary without turning the runtime into an opaque monolith.

The Research chapter adds two things that most projects omit:

1. **Evolution narrative**: how the architecture arrived at its current shape, including the dead ends that were abandoned
2. **Academic grounding**: BibTeX entries, design pattern citations, and comparative analysis with industrial serving systems

## Suggested reading path

1. Read the [Architecture Atlas](/en/architecture/) for the system shape
2. Use [Comparisons](/en/reference/comparisons) to situate the project among adjacent serving options
3. Read [Evolution](/en/research/evolution) for the historical reasoning behind each boundary
4. Use [Academic Citations](/en/citations) when you need the upstream technical lineage
5. Finish in [Academy](/en/academy/) for pattern-level reasoning
