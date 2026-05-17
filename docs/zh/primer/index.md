# 导读

导读章节用于把读者从“刚看到仓库”快速带到“已经理解这个系统为什么值得看”。如果你想先抓住项目边界、模型范围和阅读路径，从这里开始。

## YOLO-Toys 本质上是什么

YOLO-Toys 是一个 **多模型视觉推理服务运行时**。它把多个视觉模型家族统一到一套 FastAPI 与 WebSocket 接口之下，既方便快速集成 demo / backend，也方便研究混合视觉工作负载的服务化架构。

## 先理解哪些表面

| 接口面 | 作用 |
| --- | --- |
| `/infer` | 统一检测、分割、姿态与开放词汇检测 |
| `/caption` 与 `/vqa` | BLIP 驱动的视觉语言能力 |
| `/ws` | 实时帧流推理，适合低延迟交互 |
| `/models` 与 `/labels` | 运行时发现模型与标签信息 |
| `/metrics`、`/health`、`/system/*` | 观测、诊断与运行时护栏 |

## 建议阅读顺序

1. 先看 [快速开始](/zh/getting-started/quickstart)
2. 想本地开发就继续看 [安装](/zh/getting-started/installation)
3. 想知道如何落地部署就看 [部署概览](/zh/deployment/)
4. 想深入理解设计边界就进入 [架构图谱](/zh/architecture/)

## 当前纳入的平台模型家族

| 家族 | 代表模型 | 主要职责 |
| --- | --- | --- |
| YOLOv8 | `yolov8n.pt`、`yolov8n-seg.pt`、`yolov8n-pose.pt` | 快速检测、分割、姿态 |
| DETR | `facebook/detr-resnet-50` | Transformer 检测 |
| OWL-ViT / Grounding DINO | `google/owlvit-base-patch32` | 开放词汇检测 |
| BLIP | `Salesforce/blip-image-captioning-base` | 图像描述与 VQA |

## 下一跳

- 想看系统全貌，进入 [架构图谱](/zh/architecture/)
- 想看设计原理，进入 [学院](/zh/academy/)
- 想看接口与模型矩阵，进入 [参考](/zh/reference/)
- 想看论文与竞品，进入 [研究](/zh/research/)
