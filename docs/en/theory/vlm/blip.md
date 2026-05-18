---
title: "BLIP: Image Captioning and VQA"
---

# BLIP: Bootstrapping Language-Image Pre-training

BLIP (Bootstrapping Language-Image Pre-training) is a unified vision-language model for both understanding and generation tasks. YOLO-Toys uses BLIP for image captioning and visual question answering.

## Tasks

### Image Captioning

Generate natural language descriptions of images:

```
Input: [Image]
Output: "A golden retriever playing with a red ball in a sunny park"
```

### Visual Question Answering (VQA)

Answer questions about image content:

```
Input: [Image] + "What color is the dog's collar?"
Output: "blue"
```

## Architecture

BLIP uses a unified architecture with three components:

```
┌─────────────────────────────────────────────────────────────┐
│                      BLIP Architecture                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐              ┌─────────────┐              │
│  │   Vision    │              │    Text     │              │
│  │   Encoder   │              │   Encoder   │              │
│  │  (ViT)      │              │  (BERT)     │              │
│  └─────────────┘              └─────────────┘              │
│         │                            │                     │
│         └────────────┬───────────────┘                     │
│                      │                                     │
│                      ▼                                     │
│         ┌─────────────────────────┐                        │
│         │   Multimodal Encoder    │                        │
│         │   (Image + Text)        │                        │
│         └─────────────────────────┘                        │
│                      │                                     │
│         ┌────────────┴────────────┐                        │
│         │                         │                        │
│         ▼                         ▼                        │
│  ┌─────────────┐          ┌─────────────┐                 │
│  │  Understanding│        │  Generation │                 │
│  │  Head        │          │  Head       │                 │
│  └─────────────┘          └─────────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Key innovations

### 1. Bootstrap training

BLIP bootstraps training by using a captioning model to generate synthetic captions, then filters them with a learning-based filter:

```python
# Bootstrap loop
captions = generate_captions(images)
filtered = filter_captions(captions, images)
train_on(images, filtered)
```

### 2. Unified architecture

Same model handles both understanding (VQA) and generation (captioning):

- **Understanding**: Encode image + question, predict answer
- **Generation**: Encode image, decode caption token by token

### 3. Noise injection

Add noise to text inputs during training for robustness:

```python
noisy_text = add_noise(text, prob=0.1)
```

## Model variants

| Model | Params | Caption Quality | VQA Accuracy |
|-------|--------|-----------------|--------------|
| BLIP-base | 223M | Good | 75.0% |
| BLIP-large | 582M | Better | 78.3% |

## Usage in YOLO-Toys

### Image Captioning

```python
# POST /api/v1/inference/blip
{
  "model": "Salesforce/blip-image-captioning-base",
  "image": "<base64_image>"
}

# Response
{
  "caption": "A dog playing in the park"
}
```

### Visual QA

```python
# POST /api/v1/inference/blip
{
  "model": "Salesforce/blip-vqa-base",
  "image": "<base64_image>",
  "question": "What is the dog doing?"
}

# Response
{
  "answer": "playing"
}
```

## Performance

### Image Captioning (COCO test)

| Model | BLEU-4 | METEOR | CIDEr |
|-------|--------|--------|-------|
| Show-Tell | 30.3 | 25.6 | 94.6 |
| OSCAR | 36.5 | 30.3 | 116.4 |
| BLIP | **39.9** | **32.1** | **133.2** |

### VQA (VQAv2 test-dev)

| Model | Accuracy |
|-------|----------|
| LXMERT | 72.5% |
| ViLT | 73.0% |
| BLIP | **78.3%** |

## When to use BLIP

::: tip Image Captioning
- Generate alt text for accessibility
- Create image descriptions for search
- Summarize visual content
:::

::: tip Visual QA
- Answer questions about image content
- Extract specific information from images
- Interactive image exploration
:::

## References

1. Li, J., et al. "BLIP: Bootstrapping Language-Image Pre-training." ICML 2023. [arXiv:2201.12086](https://arxiv.org/abs/2201.12086)

---

## What to read next

- [OWL-ViT](/en/theory/vlm/owl-vit) for open-vocabulary detection
- [Grounding DINO](/en/theory/vlm/grounding-dino) for phrase grounding
