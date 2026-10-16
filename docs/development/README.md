# Orbit Security: development

This package declares Python `>=3.11,<3.15`. The supported range in `pyproject.toml` does not
replace the evidence from hosted CI for each interpreter.

## Local checks

```bash
python -m pip install -e ../orbit-core
python -m pip install -e '.[dev]'
pytest
ruff check src tests
ruff format --check src tests
mypy
python -m build
```

`pytest` includes deterministic token accounting tests and ASGI middleware tests using
`orbit-testing`; no external service is required. The limiter's optional `now` argument exists to
make clock and refill behavior deterministic in tests. Application code should omit it and use the
monotonic clock.

The current local quality matrix passes on CPython 3.11, 3.12, 3.13, and 3.14: all 24 tests, Ruff
lint and format checks, strict mypy, and wheel/sdist builds pass on each interpreter. These
deterministic local checks do not establish hosted CI results or behavior under multi-process,
distributed, or production traffic.

## Contribution guidance

Keep state bounded and synchronized, validate all public configuration, and preserve unrelated
response headers. Add focused tests for invalid values, concurrent decisions, clock rollback,
eviction, rejected-request short-circuiting, response header behavior, and cancellation where a
change affects those paths. Document whether a control is process-local or distributed. New
identity or authorization behavior belongs in the corresponding capability package, not in this
rate-limiter module.
