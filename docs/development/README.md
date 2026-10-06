# orbit-security development

```bash
python -m pip install -e ../orbit-core
python -m pip install -e '.[dev]'
pytest
ruff check src tests
ruff format --check src tests
mypy
python -m build
```

Keep middleware deterministic and bounded. Test invalid limits and keys, clock behavior, eviction,
response headers, and request cancellation. Any future control must have a distinct contract and
must not quietly become an authentication implementation.
