# 安装指南

本指南介绍在系统上安装和配置 YOLO-Toys 的所有方式。

---

## 📋 系统要求

### 最低要求

| 组件 | 要求 |
|-----------|-------------|
| **Python** | 3.11 或更高版本 |
| **内存** | 4 GB（推荐 8 GB+） |
| **存储** | 2 GB 可用空间 |
| **操作系统** | Linux、macOS 或 Windows |

### GPU 支持（可选）

| 硬件 | 要求 |
|----------|--------------|
| **NVIDIA** | CUDA 11.8+ 及 cuDNN |
| **Apple Silicon** | macOS 12.3+ 支持 MPS |
| **AMD** | ROCm（社区支持） |

---

## 🐍 方式一：Python 原生（推荐开发使用）

### 步骤 1：克隆仓库

```bash
git clone https://github.com/LessUp/yolo-toys.git
cd yolo-toys
```

### 步骤 2：创建虚拟环境

```bash
# 创建虚拟环境
python -m venv .venv

# 激活（Linux/macOS）
source .venv/bin/activate

# 激活（Windows PowerShell）
.venv\Scripts\Activate.ps1
```

### 步骤 3：安装依赖

```bash
# 安装运行时依赖
pip install -r requirements.txt

# （可选）安装开发依赖
pip install -r requirements-dev.txt
```

### 步骤 4：配置环境

```bash
# 复制示例环境文件
cp .env.example .env

# 编辑 .env 自定义设置
```

### 步骤 5：验证安装

```bash
# 运行 lint 验证设置
make lint

# 运行测试
make test
```

---

## 🐳 方式二：Docker

### Docker 快速开始

```bash
# 克隆仓库
git clone https://github.com/LessUp/yolo-toys.git
cd yolo-toys

# 复制环境文件
cp .env.example .env

# 构建并运行
docker build -t yolo-toys .
docker run -p 8000:8000 --env-file .env yolo-toys
```

### 使用 Docker Compose（推荐生产环境）

```bash
docker-compose up --build -d
```

---

## ✅ 下一步

- [快速开始](./quickstart) — 运行你的第一次检测
- [API 参考](../api/rest-api) — 学习 API
- [部署指南](../deployment/docker) — 生产环境部署
