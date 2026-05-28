# 2026-05-28 CPU-only PyTorch 支持

## 变更内容

### 修改文件

- `pyproject.toml`: 放宽 PyTorch 版本约束
  - `torch~=2.3.0` → `torch>=2.3.0`
  - `torchvision~=0.18.0` → `torchvision>=0.18.0`

### 原因

用户在 Python 3.13 环境下运行 `uv sync` 时遇到错误：
- PyTorch 2.3.1 不支持 Python 3.13（只有 cp311、cp312 wheels）
- 项目配置要求 Python >= 3.11，但锁定 torch~=2.3.0

### 解决方案

1. 使用 Python 3.12 创建虚拟环境
2. 安装 CPU-only PyTorch（约 200MB，而非 CUDA 版本的 2GB+）
3. 放宽版本约束，允许安装更新的 PyTorch 版本

### 验证结果

```
Python: 3.12.2
PyTorch: 2.12.0+cpu
CUDA available: False
```

## 备注

项目完全支持 CPU-only 运行：
- 代码自动检测 CUDA/MPS/CPU 设备
- 所有测试默认使用 CPU
- 可通过 `DEVICE=cpu` 环境变量强制使用 CPU
