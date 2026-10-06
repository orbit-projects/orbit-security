# Orbit Security

`orbit-security` provides cross-cutting security controls that are separate from identity and
authentication. Its initial capability is an opt-in, bounded, in-process HTTP rate limiter for
Orbit's ASGI application.

```bash
python -m pip install orbit-core orbit-security
```

```python
from orbit import Application, ApplicationConfig
from orbit.asgi import ASGIApplication
from orbit_security import RateLimitMiddleware

application = Application(ApplicationConfig(name="orders"))
asgi = ASGIApplication(application)
asgi.add_middleware(RateLimitMiddleware(limit=120, period=60))
```

The default key uses the validated client host. Applications may provide a bounded key function
for an authenticated identity or tenant. Configure Core's trusted forwarded-header policy before
relying on proxy-provided addresses.

This limiter is local to one process and does not provide a shared quota across workers or hosts.
Use an upstream or separately installable distributed control when deployment-wide enforcement is
required. Authentication and authorization live in `orbit-auth`; provider integrations use the
`orbit-auth-*` package family.

This package is pre-alpha and is not a production certification.

## Documentation and development

Read the [architecture](docs/architecture/overview.md), [operations](docs/operations/README.md),
[security](docs/security/overview.md), and [development](docs/development/README.md) guides.

```bash
python -m pip install -e ../orbit-core
python -m pip install -e '.[dev]'
pytest
ruff check src tests
ruff format --check src tests
mypy
python -m build
```

Licensed under Apache-2.0.
