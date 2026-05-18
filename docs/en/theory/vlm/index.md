---
title: Vision-Language Models
---

# Vision-Language Models

Vision-language models (VLMs) bridge the gap between visual perception and natural language understanding. YOLO-Toys serves several VLMs for open-vocabulary detection, image captioning, and visual question answering.

## Why vision-language models?

Traditional vision models have a fundamental limitation: they only understand categories they were trained on. VLMs overcome this by learning from image-text pairs, enabling:

1. **Open-vocabulary detection**: Detect objects described in natural language
2. **Image captioning**: Generate natural language descriptions
3. **Visual QA**: Answer questions about image content

## Models in YOLO-Toys

### [OWL-ViT](/en/theory/vlm/owl-vit)

Open-vocabulary object detection using contrastive pre-training.

- **Task**: Text-conditioned detection
- **Input**: Image + text queries
- **Output**: Bounding boxes for each query
- **Use case**: Detect arbitrary objects without training

### [Grounding DINO](/en/theory/vlm/grounding-dino)

Phrase grounding with fused vision-language features.

- **Task**: Phrase grounding (link text to image regions)
- **Input**: Image + text description
- **Output**: Bounding boxes for each phrase
- **Use case**: Detailed scene understanding

### [BLIP](/en/theory/vlm/blip)

Bootstrapping Language-Image Pre-training for unified vision-language understanding and generation.

- **Task**: Image captioning, visual QA
- **Input**: Image (± text question)
- **Output**: Natural language description/answer
- **Use case**: Content understanding, accessibility

## Comparison

| Model | Task | Open-vocab | Output |
|-------|------|------------|--------|
| OWL-ViT | Detection | ✓ | Boxes |
| Grounding DINO | Grounding | ✓ | Boxes |
| BLIP | Caption/VQA | N/A | Text |

## What to read next

- [OWL-ViT](/en/theory/vlm/owl-vit) for open-vocabulary detection
- [Grounding DINO](/en/theory/vlm/grounding-dino) for phrase grounding
- [BLIP](/en/theory/vlm/blip) for captioning and VQA
