# Docker 部署

使用 Docker 容器部署 YOLO-Toys。

---

## 📋 前提条件

- Docker 20.10+
- Docker Compose 2.0+（可选）
- 4GB+ 可用内存
- 2GB+ 可用磁盘空间

---

## 🚀 快速开始

### 使用 Docker Run

```bash
# 克隆仓库
git clone https://github.com/LessUp/yolo-toys.git
cd yolo-toys

# 复制环境配置
cp .env.example .env

# 构建并运行
docker build -t yolo-toys .
docker run -d -p 8000:8000 --env-file .env yolo-toys
```

### 使用 Docker Compose（推荐）

```bash
docker-compose up -d
```

---

## ⚙️ docker-compose.yml 参考

```yaml
services:
  yolo-toys:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_NAME=yolov8n.pt
      - DEVICE=cpu
    volumes:
      - model-cache:/root/.cache
    restart: unless-stopped

volumes:
  model-cache:
```

---

## 🖥️ GPU 支持

### NVIDIA GPU

```yaml
services:
  yolo-toys:
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - DEVICE=cuda:0
```

---

## 🔧 生产环境部署

### 反向代理（Nginx）

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }
}
```

---

## 🔗 相关文档

- [安装](../getting-started/installation) — 原生安装
- [环境变量](./environments) — 配置参考
- [架构](../architecture/overview) — 系统设计
