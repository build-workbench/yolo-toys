# 部署

将 YOLO-Toys 部署到生产环境。

## 部署选项

| 环境 | 适用场景 | 指南 |
|-------------|----------|-------|
| Docker | 生产服务器 | [Docker](./docker) |
| Docker Compose | 多服务部署 | [Docker](./docker) |
| 云 | 可扩展部署 | [环境配置](./environments) |

## 快速部署

```bash
# 单容器
docker run -p 8000:8000 ghcr.io/lessup/yolo-toys:latest

# 使用 docker-compose
docker-compose up -d
```
