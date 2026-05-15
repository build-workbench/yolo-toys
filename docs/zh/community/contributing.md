---
title: 贡献指南
---

# 贡献到 YOLO-Toys

感谢您有兴趣贡献！本指南涵盖您需要知道的一切。

## 快速开始

### 1. Fork 和 Clone

```bash
# 在 GitHub 上 Fork，然后 clone
git clone https://github.com/YOUR-USERNAME/yolo-toys.git
cd yolo-toys

# 添加上游远程
git remote add upstream https://github.com/your-org/yolo-toys.git
```

### 2. 设置开发环境

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或：.venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 安装 pre-commit hooks
pre-commit install
```

### 3. 进行更改

```bash
# 创建分支
git checkout -b feature/my-feature

# 进行更改
# ...

# 运行测试
make test

# 运行 linter
make lint
```

### 4. 提交 Pull Request

```bash
# Push 到你的 fork
git push origin feature/my-feature

# 在 GitHub 上打开 PR
```

## 开发工作流

### 分支命名

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能 | `feature/add-sam-support` |
| `fix/` | 错误修复 | `fix/cache-eviction-race` |
| `docs/` | 文档 | `docs/api-examples` |
| `refactor/` | 代码重构 | `refactor/handler-interface` |

### 提交消息

遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/)：

```
<类型>(<范围>): <描述>

[可选正文]

[可选脚注]
```

**类型**：
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档
- `style`: 格式化（无代码更改）
- `refactor`: 重构
- `test`: 添加测试
- `chore`: 维护

**示例**：
```
feat(handler): 添加 SAM（Segment Anything）支持

为 Meta 的 Segment Anything Model 添加新 Handler，
支持框和点提示。

Closes #123
```

## 代码风格

### Python

我们使用 Ruff 进行 linting 和格式化：

```bash
# 格式化代码
make format  # 或：ruff format .

# 检查 lint
make lint    # 或：ruff check .
```

### 关键风格规则

1. **类型提示**：所有公共 API 使用
   ```python
   def load_model(self, model_id: str) -> LoadedModel:
       ...
   ```

2. **文档字符串**：所有公共函数使用 Google 风格
   ```python
   def infer(self, image: np.ndarray, params: InferenceParams) -> dict:
       """
       执行推理。

       Args:
           image: 输入图像（BGR numpy 数组）。
           params: 推理参数。

       Returns:
           带检测结果的结果字典。
       """
   ```

3. **行长度**：88 字符（Black 默认）

4. **导入**：使用 `isort` 排序

## 测试

### 运行测试

```bash
# 所有测试
make test

# 特定测试文件
pytest tests/test_handlers.py

# 带覆盖率
pytest --cov=app tests/
```

### 测试指南

1. **Mock 模型加载**用于单元测试：
   ```python
   @pytest.fixture
   def mock_model():
       with patch("app.handlers.yolo_handler.YOLO"):
           yield
   ```

2. **使用测试图像**从 `tests/fixtures/`：
   ```python
   @pytest.fixture
   def test_image():
       return cv2.imread("tests/fixtures/test.jpg")
   ```

3. **不测试外部服务**：
   - Mock HuggingFace Hub 调用
   - CI 中不需要真实 GPU

## 添加新模型

参阅[自定义 Handler 指南](/zh/guides/custom-handler)了解详细步骤。

### 检查清单

- [ ] 添加 `ModelCategory` 枚举值
- [ ] 创建继承 `BaseHandler` 的 Handler 类
- [ ] 实现 `_do_load` 和 `_infer_impl`
- [ ] 在 `_CATEGORY_HANDLER_MAP` 中注册
- [ ] 添加到 `MODEL_REGISTRY`
- [ ] 编写单元测试
- [ ] 更新文档

## Pull Request 流程

### 提交前

- [ ] 代码通过 `make lint`
- [ ] 测试通过 `make test`
- [ ] 文档已更新
- [ ] 提交消息遵循约定
- [ ] 分支与 main 保持同步

### PR 模板

```markdown
## 描述
简要描述更改。

## 更改类型
- [ ] 错误修复
- [ ] 新功能
- [ ] 破坏性更改
- [ ] 文档

## 测试
如何测试的？

## 检查清单
- [ ] 测试通过
- [ ] Lint 干净
- [ ] 文档已更新
```

### 审查流程

1. **自动检查**运行（lint、test）
2. **维护者审查**在 48 小时内
3. **处理反馈**在新提交中
4. **Squash 并合并**当批准后

### 合并后

- 你的贡献出现在发布说明中
- 你被添加到贡献者列表

## 获取帮助

- **GitHub Discussions**：一般问题
- **Discord**：实时帮助
- **代码评论**：在 PR 中询问

## 认可

贡献者在以下获得认可：
- 每次发布的 `CHANGELOG.md`
- GitHub 贡献者页面
- 年度贡献者亮点
