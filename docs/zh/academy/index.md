---
title: 学院 - 深度学习模式
---

# YOLO-Toys 学院

欢迎来到 YOLO-Toys 学院，这是一份精选的深度技术探索文集，深入剖析支撑多模型视觉推理平台的核心架构模式。

## 目的

学院模块作为知识库，面向希望理解我们设计决策背后"为什么"的开发者。每篇文章超越 API 文档层面，深入探讨理论基础、权衡考量和实际实现细节。

## 你将学到什么

### 设计模式

| 模式 | 描述 | 文章 |
|------|------|------|
| **Handler 模式** | 多模型统一推理的策略模式 | [深度解析 →](/zh/academy/handler-pattern) |
| **Registry 模式** | 集中式元数据管理与模型发现 | [深度解析 →](/zh/academy/registry-pattern) |
| **缓存策略** | 内存压力感知的 TTL + LRU 混合驱逐 | [深度解析 →](/zh/academy/caching-strategy) |
| **OpenSpec 规范** | 基于 Gherkin 的行为契约定义 | [深度解析 →](/zh/academy/openspec-system) |

## 学习路径

建议按以下顺序阅读：

```
┌─────────────────────────────────────────────────────────────┐
│                    学习路径                                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. Handler 模式 ──▶ 核心抽象层                              │
│          │                                                   │
│          ▼                                                   │
│   2. Registry 模式 ──▶ 模型发现与路由                         │
│          │                                                   │
│          ▼                                                   │
│   3. 缓存策略 ──▶ 性能优化                                    │
│          │                                                   │
│          ▼                                                   │
│   4. OpenSpec 规范 ──▶ 行为规范                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 目标读者

- **后端工程师**：希望实现类似多模型系统
- **机器学习工程师**：关注生产部署模式
- **软件架构师**：评估设计权衡
- **贡献者**：希望扩展 YOLO-Toys 新模型

## 文章标准

每篇学院文章遵循一致的结构：

1. **问题陈述** - 我们要解决什么挑战？
2. **理论基础** - 软件设计文献中的模式
3. **实现深度解析** - 带图表的代码层面分析
4. **权衡考量** - 我们获得了什么，牺牲了什么
5. **扩展指南** - 如何定制或扩展该模式

## 快速参考

### 模型类别

| 类别 | 任务 | Handler 类 |
|------|------|------------|
| `yolo_detect` | 目标检测 | `YOLOHandler` |
| `yolo_segment` | 实例分割 | `YOLOHandler` |
| `yolo_pose` | 姿态估计 | `YOLOHandler` |
| `hf_detr` | 检测（Transformer） | `DETRHandler` |
| `hf_owlvit` | 开放词汇检测 | `OWLViTHandler` |
| `hf_grounding_dino` | 基于文本的检测 | `GroundingDINOHandler` |
| `multimodal_caption` | 图像描述 | `BLIPCaptionHandler` |
| `multimodal_vqa` | 视觉问答 | `BLIPVQAHandler` |

### 核心抽象

```python
# YOLO-Toys 架构的三大支柱
BaseHandler      # 模型推理的策略接口
HandlerRegistry  # 模型解析的中央调度器
ModelManager     # 带缓存和生命周期管理的外观类
```

## 贡献

发现错误或想添加文章？请参阅[贡献指南](/zh/community/contributing)了解如何提交学院改进。
