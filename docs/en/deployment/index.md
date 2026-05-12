# Deployment

Deploy YOLO-Toys to production environments.

## Deployment Options

| Environment | Best For | Guide |
|-------------|----------|-------|
| Docker | Production servers | [Docker](./docker) |
| Docker Compose | Multi-service setups | [Docker](./docker) |
| Cloud | Scalable deployments | [Environments](./environments) |

## Quick Deploy

```bash
# Single container
docker run -p 8000:8000 ghcr.io/lessup/yolo-toys:latest

# With docker-compose
docker-compose up -d
```
