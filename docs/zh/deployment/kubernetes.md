---
title: Kubernetes 部署
---

# Kubernetes 部署

本指南介绍如何在 Kubernetes 集群中部署 YOLO-Toys。

## 前置要求

- Kubernetes 1.24+
- NVIDIA GPU Operator
- 支持 GPU 的节点

## 部署清单

### Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: yolo-toys
```

### Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yolo-toys
  namespace: yolo-toys
spec:
  replicas: 1
  selector:
    matchLabels:
      app: yolo-toys
  template:
    metadata:
      labels:
        app: yolo-toys
    spec:
      containers:
      - name: yolo-toys
        image: ghcr.io/lessup/yolo-toys:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "4Gi"
          requests:
            memory: "2Gi"
        env:
        - name: ENABLE_FP16
          value: "true"
        volumeMounts:
        - name: model-cache
          mountPath: /app/.cache
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: model-cache
        emptyDir: {}
```

### Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: yolo-toys
  namespace: yolo-toys
spec:
  selector:
    app: yolo-toys
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: yolo-toys
  namespace: yolo-toys
spec:
  rules:
  - host: yolo-toys.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: yolo-toys
            port:
              number: 80
```

## 部署步骤

```bash
# 创建命名空间
kubectl apply -f namespace.yaml

# 部署应用
kubectl apply -f deployment.yaml

# 创建服务
kubectl apply -f service.yaml

# 配置 Ingress
kubectl apply -f ingress.yaml
```

## 自动扩缩容

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: yolo-toys-hpa
  namespace: yolo-toys
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: yolo-toys
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 故障排查

### Pod 无法启动

```bash
kubectl describe pod -n yolo-toys <pod-name>
kubectl logs -n yolo-toys <pod-name>
```

### GPU 不可用

确认 GPU Operator 正常运行：

```bash
kubectl get pods -n gpu-operator
kubectl describe node <gpu-node> | grep nvidia.com/gpu
```
