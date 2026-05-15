---
title: Contributing Guide
---

# Contributing to YOLO-Toys

Thank you for your interest in contributing! This guide covers everything you need to know.

## Quick Start

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone
git clone https://github.com/YOUR-USERNAME/yolo-toys.git
cd yolo-toys

# Add upstream remote
git remote add upstream https://github.com/your-org/yolo-toys.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 3. Make Your Changes

```bash
# Create a branch
git checkout -b feature/my-feature

# Make changes
# ...

# Run tests
make test

# Run linters
make lint
```

### 4. Submit Pull Request

```bash
# Push to your fork
git push origin feature/my-feature

# Open PR on GitHub
```

## Development Workflow

### Branch Naming

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New feature | `feature/add-sam-support` |
| `fix/` | Bug fix | `fix/cache-eviction-race` |
| `docs/` | Documentation | `docs/api-examples` |
| `refactor/` | Code refactoring | `refactor/handler-interface` |

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Refactoring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```
feat(handler): add SAM (Segment Anything) support

Add a new handler for Meta's Segment Anything Model,
supporting both box and point prompts.

Closes #123
```

## Code Style

### Python

We use Ruff for linting and formatting:

```bash
# Format code
make format  # or: ruff format .

# Check lint
make lint    # or: ruff check .
```

### Key Style Rules

1. **Type hints**: Use for all public APIs
   ```python
   def load_model(self, model_id: str) -> LoadedModel:
       ...
   ```

2. **Docstrings**: Google style for all public functions
   ```python
   def infer(self, image: np.ndarray, params: InferenceParams) -> dict:
       """
       Execute inference.

       Args:
           image: Input image (BGR numpy array).
           params: Inference parameters.

       Returns:
           Result dictionary with detections.
       """
   ```

3. **Line length**: 88 characters (Black default)

4. **Imports**: Use `isort` ordering

### Pre-commit Hooks

Hooks run automatically on commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
      - id: ruff-format
```

## Testing

### Run Tests

```bash
# All tests
make test

# Specific test file
pytest tests/test_handlers.py

# With coverage
pytest --cov=app tests/
```

### Test Guidelines

1. **Mock model loading** for unit tests:
   ```python
   @pytest.fixture
   def mock_model():
       with patch("app.handlers.yolo_handler.YOLO"):
           yield
   ```

2. **Use test images** from `tests/fixtures/`:
   ```python
   @pytest.fixture
   def test_image():
       return cv2.imread("tests/fixtures/test.jpg")
   ```

3. **Don't test external services**:
   - Mock HuggingFace Hub calls
   - Don't require real GPU in CI

### Test Categories

| Marker | Purpose | Command |
|--------|---------|---------|
| `unit` | Fast, no I/O | `pytest -m unit` |
| `integration` | API tests | `pytest -m integration` |
| `slow` | Long-running | `pytest -m "not slow"` |

## Documentation

### Update Docs When

- Adding new API endpoints
- Changing existing behavior
- Adding new models
- Fixing documented bugs

### Docs Location

| Type | Location |
|------|----------|
| API docs | `docs/en/api/` |
| Architecture | `docs/en/architecture/` |
| Guides | `docs/en/guides/` |
| Reference | `docs/en/reference/` |

### Preview Docs

```bash
cd docs
npm install
npm run docs:dev
```

## Adding a New Model

See [Custom Handler Guide](/en/guides/custom-handler) for detailed steps.

### Checklist

- [ ] Add `ModelCategory` enum value
- [ ] Create handler class inheriting `BaseHandler`
- [ ] Implement `_do_load` and `_infer_impl`
- [ ] Register in `_CATEGORY_HANDLER_MAP`
- [ ] Add to `MODEL_REGISTRY`
- [ ] Write unit tests
- [ ] Update documentation

## Pull Request Process

### Before Submitting

- [ ] Code passes `make lint`
- [ ] Tests pass `make test`
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Lint clean
- [ ] Docs updated
```

### Review Process

1. **Automated checks** run (lint, test)
2. **Maintainer review** within 48 hours
3. **Address feedback** in new commits
4. **Squash and merge** when approved

### After Merge

- Your contribution appears in release notes
- You're added to contributors list

## Release Process

Maintainers follow this process:

1. Update version in `app/__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag
4. Build and push Docker image
5. Create GitHub release

## Getting Help

- **GitHub Discussions**: General questions
- **Discord**: Real-time help
- **Code comments**: Ask in PR

## Recognition

Contributors are recognized in:
- `CHANGELOG.md` for each release
- GitHub contributors page
- Annual contributor highlights
