---
title: 错误码参考
---

# 错误码参考

YOLO-Toys API 使用标准 HTTP 状态码和自定义错误码来表示错误情况。

## HTTP 状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 400 | Bad Request | 请求参数错误 |
| 404 | Not Found | 资源不存在 |
| 422 | Unprocessable Entity | 无法处理的实体 |
| 500 | Internal Server Error | 服务器内部错误 |
| 503 | Service Unavailable | 服务不可用 |

## 错误响应格式

所有错误响应遵循统一格式：

```json
{
  "detail": "错误描述信息",
  "error_code": "ERROR_CODE",
  "context": {
    "additional": "上下文信息"
  }
}
```

## 模型相关错误

| 错误码 | 说明 |
|--------|------|
| `MODEL_NOT_FOUND` | 请求的模型不存在 |
| `MODEL_LOAD_FAILED` | 模型加载失败 |
| `MODEL_INFER_FAILED` | 模型推理失败 |
| `MODEL_TIMEOUT` | 模型加载超时 |

## 图片相关错误

| 错误码 | 说明 |
|--------|------|
| `IMAGE_DECODE_FAILED` | 图片解码失败 |
| `IMAGE_TOO_LARGE` | 图片尺寸过大 |
| `INVALID_IMAGE_FORMAT` | 无效的图片格式 |

## 参数相关错误

| 错误码 | 说明 |
|--------|------|
| `INVALID_CONFIDENCE` | 无效的置信度阈值 |
| `INVALID_IOU_THRESHOLD` | 无效的 IOU 阈值 |
| `MISSING_REQUIRED_PARAM` | 缺少必需参数 |

## 服务相关错误

| 错误码 | 说明 |
|--------|------|
| `SERVICE_UNAVAILABLE` | 服务暂时不可用 |
| `GPU_MEMORY_EXHAUSTED` | GPU 内存不足 |
| `RATE_LIMIT_EXCEEDED` | 请求频率超限 |

## 常见错误排查

### 模型加载失败

```json
{
  "detail": "Failed to load model yolov8x",
  "error_code": "MODEL_LOAD_FAILED"
}
```

**可能原因：**
- 模型文件未下载
- 磁盘空间不足
- GPU 内存不足

**解决方案：**
1. 检查模型缓存目录
2. 清理磁盘空间
3. 使用更小的模型变体

### GPU 内存不足

```json
{
  "detail": "CUDA out of memory",
  "error_code": "GPU_MEMORY_EXHAUSTED"
}
```

**解决方案：**
1. 使用 FP16 推理
2. 减小批处理大小
3. 使用更小的模型
4. 清理模型缓存
