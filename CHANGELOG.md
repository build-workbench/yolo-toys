# 更新日志

yolo-toys 是一个基于 FastAPI 的浏览器端目标检测与多模态推理项目，后端以统一的多模型架构支持 YOLO / DETR / OWL-ViT / BLIP 等模型。
格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增

- 摄像头实时推理：权限预检查、浏览器/HTTPS 兼容性检测，以及 info/warning/error 分级提示。
- 本地图片上传推理与检测结果侧边栏：展示检测总数、模型与设备信息、性能指标，并按检测数量列出类别分布。
- 多模型后端：引入 ModelManager 统一管理 YOLO/DETR/OWL-ViT/BLIP，新增 `/models`、`/models/{model_id}`、`/caption`、`/vqa` 端点，`/infer` 支持开放词汇检测与视觉问答。
- 前端交互：设置面板、深色/浅色主题切换、响应式侧边栏，并为关键按钮与模型卡片补充 aria-label 和键盘操作。
- 前端字体自托管（Code New Roman / Resource Han Rounded CN），移除 Google Fonts 外部依赖，支持离线使用。
- 架构分层：新增 app/dependencies.py（FastAPI 依赖注入）与 app/protocols.py + app/decoders.py（ImageDecoder / OpenCVDecoder）。
- 性能与可观测性：TTL + LRU 混合缓存、内存压力下模型自动淘汰、结构化日志与 Prometheus 指标。
- 安全：安全响应头/限流/超时中间件，pip-audit + CodeQL 安全审计工作流。
- 测试体系：测试从 6 个扩充到 100+，新增 WebSocket、边界输入、中间件、指标与处理器测试，覆盖率提升至 70%+。
- 部署：多架构 Docker 构建与 CUDA GPU 支持，新增发布工作流。

### 变更

- v3.0.0 架构重构：用策略模式拆分 model_manager.py（814 → 105 行）并新增 app/handlers/；Pydantic Settings 统一配置（app/config.py）；FastAPI lifespan 替代 on_event；路由提取到 app/routes.py，main.py 精简为 91 行；结构化日志替代 print。
- v3.1.0 文档重构：建立专业化双语文档（getting-started / api / architecture / deployment / guides / reference）与符合 Keep a Changelog 规范的 changelog。
- 工具链统一：用 Ruff 统一 lint + format（移除 black + isort），类型注解现代化到 py311+，前端转为 ES Module。
- 依赖升级：FastAPI 0.115、PyTorch 2.3、Transformers 4.44，并放宽 PyTorch 约束以支持 CPU-only 环境。
- GitHub Pages 文档站多轮迭代：Jekyll → Nextra → VitePress（YOLO Orange 主题）→ 白皮书级重构 → 站点中文化（移除英文文档树与 en locale）。
- README 收敛为单一中文入口/精简单页；CI/CD 与部署配置精简。

### 修复

- 放宽 PyTorch/torchvision 版本约束，解决 Python 3.13 与 PyTorch 2.3.1 不兼容的问题。
- 修复 basedpyright 类型错误、Ruff lint 违规、失败的测试用例与类型比较错误。
- 用 QueryParams 替换已弃用的 ImmutableMultiQueryDict。
- 修复 GitHub Actions workflow 错误、Node.js 24 兼容与 pip-audit action 版本问题。
- 修复 GitHub Pages 死链、按钮文字对比度，以及标题文字在部分浏览器不可见的问题。

### 移除

- 删除文档站、OpenSpec 规范体系与发布历史（changelog/），以及治理文件与社区模板；移除 dependabot 自动依赖更新配置。
- 移除失效的 Prometheus/Grafana monitoring 栈与 docs-pages 工作流。
