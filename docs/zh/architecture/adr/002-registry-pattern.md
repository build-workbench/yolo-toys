---
title: ADR-002 - 集中式注册表优于分布式元数据
---

# ADR-002：集中式注册表优于分布式元数据

| 状态 | 日期 | 决策者 |
|------|------|--------|
| 已采纳 | 2024-01-15 | 架构团队 |

## 背景

YOLO-Toys 需要：
1. 知道有哪些可用模型
2. 将模型 ID 映射到 Handler
3. 在 API 响应中显示模型元数据
4. 为未知模型推断类别

我们有几种组织此信息的选项：
- 中央注册表常量
- 分布在各 Handler 的元数据
- 配置文件（YAML、JSON）
- 外部数据库

## 决策

我们采用 **集中式注册表模式**：
- `MODEL_REGISTRY` 是单一的字典常量
- `ModelCategory` 枚举封装所有类别
- 类别推断逻辑在 `ModelCategory.infer_from_id()`

```python
# 单一事实来源
MODEL_REGISTRY: dict[str, dict[str, Any]] = {
    "yolov8n.pt": {
        "category": ModelCategory.YOLO_DETECT,
        "name": "YOLOv8 Nano",
        "description": "超轻量检测模型",
        "speed": "极快",
        "accuracy": "中等",
    },
    ...
}
```

## 考虑的替代方案

### 替代方案 1：分布式元数据

将元数据存储在各 Handler 旁：

```python
class YOLOHandler(BaseHandler):
    MODELS = {
        "yolov8n.pt": {"name": "YOLOv8 Nano", ...},
        "yolov8s.pt": {"name": "YOLOv8 Small", ...},
    }
```

**优点**：
- 模型信息与推理逻辑共置
- Handler 作者拥有自己的模型

**缺点**：
- 难以枚举所有模型（需导入所有 Handler）
- 类别信息分散
- 难以维护一致性
- 循环导入风险

### 替代方案 2：配置文件

将元数据存储在 YAML/JSON：

```yaml
models:
  yolov8n.pt:
    category: yolo_detect
    name: YOLOv8 Nano
```

**优点**：
- 无需修改代码即可编辑
- 可用模式验证

**缺点**：
- 与代码分离（漂移风险）
- 无类型安全
- 启动时需加载和解析
- 更难版本控制变更

## 后果

### 正面

1. **单一事实来源**：所有元数据在一处
2. **类型安全**：类别使用枚举，类型化字典
3. **可预测**：每次运行相同的模型可用
4. **简单**：字典查找，无外部依赖
5. **版本控制**：变更在 git 中追踪

### 负面

1. **集中化变更**：添加模型需要修改代码
2. **内存开销**：注册表始终在内存中
3. **无运行时更新**：添加模型需要重启

### 缓解措施

- **集中化变更**：简单的字典结构，PR 易于审查
- **内存开销**：可忽略（几 KB）
- **无运行时更新**：通过推断支持临时的 `.pt` 文件

## 参考文献

- [Registry 模式](https://martinfowler.com/eaaCatalog/registry.html)
- [单一事实来源](https://en.wikipedia.org/wiki/Single_source_of_truth)
