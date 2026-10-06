# orbit-security architecture

`orbit-security` owns cross-cutting application security controls. The first control is a bounded
process-local HTTP token-bucket limiter implemented as ASGI middleware.

```text
Orbit Core: ASGI pipeline and runtime
├── orbit-auth: authentication and authorization capabilities
└── orbit-security: cross-cutting security controls
```

The limiter uses Core's request and response contracts. It has bounded key cardinality, validates
configuration and client keys, emits standard rate-limit headers, and does not import an
authentication implementation. Applications may key quotas by authenticated principals through
an explicit callback.

This package does not provide authentication, authorization, a distributed quota store, WAF, or
upstream abuse protection. Multi-process deployments maintain one independent limiter per worker.
