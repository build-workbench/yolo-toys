# AGENTS.md — YOLO-Toys

基于 FastAPI + WebSocket 的多模型视觉推理服务：统一 YOLOv8 / DETR / OWL-ViT / Grounding DINO / BLIP，提供检测、分割、姿态、开放词汇推理、图像描述与视觉问答，并附带浏览器端实时推理前端。

## 常用命令

```bash
bash scripts/dev.sh setup   # 初始化：创建 .venv、安装 requirements.txt + requirements-dev.txt、pre-commit install
make run                    # 本地启动开发服务器：uvicorn app.main:app --reload（端口 8000）
make test                   # 运行 pytest（自动带 SKIP_WARMUP=1，默认含 --cov=app 覆盖率）
make lint                   # 非变更式检查：ruff check . + ruff format --check .
make format                 # 自动格式化：ruff check --fix . + ruff format .
make typecheck              # basedpyright 类型检查
make hooks                  # 运行全部 pre-commit 钩子
make docker-build           # 构建 Docker 镜像（make docker-build-cuda 构建 CUDA GPU 版）
make compose-up             # docker compose 启动（make compose-down 停止）
make clean                  # 清理 __pycache__、.ruff_cache、htmlcov 等缓存
```

## 代码结构

- `app/main.py` — FastAPI 入口，lifespan 管理生命周期，挂载路由、中间件与静态前端
- `app/api/` — 路由层：inference（/infer、/caption、/vqa）、models、system、websocket（WS /ws）、utils
- `app/handlers/` — 各模型推理处理器（策略模式）：base 定义接口，yolo/hf/blip_handler 实现，registry 注册
- `app/model_manager.py` — ModelManager：统一模型加载、TTL+LRU 缓存与内存压力下自动淘汰
- `app/config.py` — Pydantic Settings 统一管理环境变量；config_adapters.py、config_protocols.py 为其辅助
- `app/dependencies.py` / `app/protocols.py` / `app/decoders.py` — FastAPI 依赖注入与 ImageDecoder 图像解码
- `app/middleware.py` / `app/metrics.py` — 安全响应头、限流、超时中间件与 Prometheus 指标
- `app/schemas.py` / `app/params.py` — 请求/响应 Pydantic 模型与查询参数
- `frontend/` — 原生 JS（ES Module）前端：index.html、app.js、js/{api,camera,draw}.js，字体自托管于 fonts/
- `config/` — 环境变量样例：.env.example（Makefile 默认）、.env.development、.env.production
- `deployments/docker/` — Dockerfile、Dockerfile.cuda、docker-compose.yml
- `tests/` — pytest 测试：test_api.py、test_model_manager.py、test_coverage.py 及 test_handlers/ 按模块划分
- `scripts/dev.sh` — 开发脚本，子命令与 Makefile 对应（setup/run/test/lint/typecheck/format/hooks/docker/clean）

## 关键约束

- Python >= 3.11（CI 在 3.11 / 3.12 矩阵上执行 lint + test）
- Ruff 统一 lint + format（已移除 black + isort）：line-length 100、target py311；RUF001–003 已忽略以允许中文字符串/注释
- 类型检查用 basedpyright（standard 模式），unknown 类规则降级为 warning；需 py311+ 风格类型注解
- 测试需 `SKIP_WARMUP=1`（make test 已内置）；pytest 默认带 `--cov=app`，覆盖率阈值 fail_under = 15，app/main.py 不计覆盖率
- CI（.github/workflows/ci.yml）依次执行 ruff check、ruff format --check、pytest --cov-report=xml、pip-audit
- 配置一律通过 Pydantic Settings（app/config.py）读取环境变量，不硬编码；新增端点需接入 app/api/ 路由与 schemas

## 文档约定

- CHANGELOG.md：面向用户的变更在合入时写入 [Unreleased]（Keep a Changelog zh-CN 格式）
- 文档全中文
