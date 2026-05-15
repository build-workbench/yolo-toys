---
title: Kubernetes Deployment Guide
---

# Kubernetes Deployment Guide

This guide covers deploying YOLO-Toys to Kubernetes for production workloads.

## Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- GPU node pool (optional, recommended)
- Container registry access

## Deployment Manifest

### Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: yolo-toys
```

### ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: yolo-toys-config
  namespace: yolo-toys
data:
  MODEL_NAME: "yolov8s.pt"
  CONF_THRESHOLD: "0.25"
  IOU_THRESHOLD: "0.45"
  MAX_CONCURRENCY: "8"
  MODEL_CACHE_MAXSIZE: "10"
  MODEL_CACHE_TTL: "3600"
  MODEL_MEMORY_THRESHOLD: "0.80"
  LOG_LEVEL: "INFO"
```

### Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: yolo-toys-secret
  namespace: yolo-toys
type: Opaque
stringData:
  # Add any sensitive configuration here
  ALLOW_ORIGINS: "https://your-frontend.com"
```

### Deployment (GPU)

```yaml
# deployment-gpu.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yolo-toys
  namespace: yolo-toys
spec:
  replicas: 2
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
        image: your-registry/yolo-toys:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: yolo-toys-config
        - secretRef:
            name: yolo-toys-secret
        env:
        - name: DEVICE
          value: "cuda:0"
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
            nvidia.com/gpu: 1
          limits:
            memory: "8Gi"
            cpu: "4"
            nvidia.com/gpu: 1
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
          initialDelaySeconds: 10
          periodSeconds: 5
        volumeMounts:
        - name: model-cache
          mountPath: /app/models
      volumes:
      - name: model-cache
        emptyDir:
          sizeLimit: 5Gi
      nodeSelector:
        accelerator: nvidia-tesla-t4
      tolerations:
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
```

### Deployment (CPU Only)

```yaml
# deployment-cpu.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yolo-toys
  namespace: yolo-toys
spec:
  replicas: 3
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
        image: your-registry/yolo-toys:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: yolo-toys-config
        env:
        - name: DEVICE
          value: "cpu"
        - name: MAX_CONCURRENCY
          value: "4"
        resources:
          requests:
            memory: "2Gi"
            cpu: "2"
          limits:
            memory: "4Gi"
            cpu: "4"
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
          initialDelaySeconds: 10
          periodSeconds: 5
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
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "20m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
spec:
  ingressClassName: nginx
  rules:
  - host: yolo-api.your-domain.com
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

## Horizontal Pod Autoscaler

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
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

## Prometheus Monitoring

### ServiceMonitor

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: yolo-toys
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: yolo-toys
  namespaceSelector:
    matchNames:
    - yolo-toys
  endpoints:
  - port: http
    path: /metrics
    interval: 15s
```

### PrometheusRule

```yaml
# prometheusrule.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: yolo-toys-alerts
  namespace: monitoring
spec:
  groups:
  - name: yolo-toys
    rules:
    - alert: YoloToysHighLatency
      expr: histogram_quantile(0.99, rate(inference_duration_seconds_bucket[5m])) > 0.5
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: High inference latency
        description: P99 latency > 500ms for 5 minutes

    - alert: YoloToysHighErrorRate
      expr: rate(inference_requests_total{status="error"}[5m]) / rate(inference_requests_total[5m]) > 0.01
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: High error rate
        description: Error rate > 1% for 5 minutes

    - alert: YoloToysMemoryPressure
      expr: model_memory_usage_ratio > 0.9
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: Memory pressure detected
        description: Memory usage > 90%
```

## Deployment Commands

```bash
# Apply all manifests
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment-gpu.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
kubectl apply -f hpa.yaml

# Check deployment status
kubectl get pods -n yolo-toys
kubectl logs -f deployment/yolo-toys -n yolo-toys

# Scale manually
kubectl scale deployment yolo-toys --replicas=5 -n yolo-toys

# Rolling update
kubectl set image deployment/yolo-toys yolo-toys=your-registry/yolo-toys:v2 -n yolo-toys

# Rollback
kubectl rollout undo deployment/yolo-toys -n yolo-toys
```

## Best Practices

### 1. Resource Planning

- **GPU pods**: 1 GPU per pod, request ~4GB memory
- **CPU pods**: 2-4 cores, request ~2GB memory
- Use resource quotas to prevent resource exhaustion

### 2. Health Checks

- Liveness probe catches deadlocks
- Readiness probe ensures model is loaded
- Set appropriate initial delays for model warmup

### 3. Model Persistence

For production, consider persistent model storage:

```yaml
volumes:
- name: model-cache
  persistentVolumeClaim:
    claimName: model-pvc
```

### 4. Graceful Shutdown

```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 10"]
```

Allows in-flight requests to complete.

### 5. Security

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```
