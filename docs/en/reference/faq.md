# Frequently Asked Questions (FAQ)

Common questions and troubleshooting tips.

---

## 🚀 Getting Started

### Q: What's the minimum hardware requirement?

**A:** For basic usage:
- CPU: Any modern processor
- RAM: 4GB minimum, 8GB recommended
- Storage: 2GB free space

For GPU acceleration:
- NVIDIA: GTX 1060 6GB or better
- Apple Silicon: M1 or newer

---

## 🐛 Installation Issues

### Q: CUDA is available but not detected

**A:** Verify PyTorch CUDA:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

If False, reinstall with correct CUDA version:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

## ⚡ Performance

### Q: How to improve inference speed?

**A:** Try these optimizations:

1. **Use smaller model:**
   ```bash
   MODEL_NAME=yolov8n.pt
   ```

2. **Reduce resolution:**
   ```javascript
   canvas.toBlob(sendFrame, 'image/jpeg', 0.7)
   ```

3. **Enable GPU:**
   ```bash
   DEVICE=cuda:0
   ```

### Q: Out of memory errors

**A:** Reduce memory usage:

```bash
MODEL_NAME=yolov8n.pt
MAX_CONCURRENCY=1
```

---

## 🎯 Model Usage

### Q: How to detect custom objects?

**A:** Use open-vocabulary detection:

```bash
curl -X POST "http://localhost:8000/infer" \
  -F "model=google/owlvit-base-patch32" \
  -F "file=@image.jpg" \
  -F "text_queries=your custom object"
```

---

## 🔗 Still Need Help?

- [Documentation](../)
- [GitHub Issues](https://github.com/LessUp/yolo-toys/issues)
