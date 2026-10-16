# Orbit Security: operations

`RateLimitMiddleware` is optional ASGI middleware backed by an in-process token bucket. It applies
to requests that pass through the `ASGIApplication` where it is registered; it does not change Core
route policy or add authentication.

```python
from orbit import Application, ApplicationConfig
from orbit.asgi import ASGIApplication
from orbit_security import RateLimitMiddleware

application = Application(ApplicationConfig(name="orders"))
asgi = ASGIApplication(application)
asgi.add_middleware(RateLimitMiddleware(limit=120, period=60, max_keys=10_000))
```

The example permits 120 token costs per key and refills the bucket over 60 seconds. Configuration
is bounded: `limit` is 1–10,000,000, `period` is positive and at most 31,536,000 seconds, and
`max_keys` is 1–1,000,000. Defaults are `max_keys=10_000`. Choose practical values for the actual
request volume and identity cardinality; maximum accepted values are validation bounds, not
recommended operating targets.

## Key selection and process scope

The default key is `request.client_host` as resolved by Core. Behind a reverse proxy, configure
Core's trusted-proxy/forwarded-header policy before relying on that address. Do not read arbitrary
`X-Forwarded-For` values yourself. A custom key function can use an authenticated principal or a
tenant ID only when authentication has already established it as trusted. Keys must be nonempty,
control-free strings of at most 255 characters.

Each middleware instance and process has independent buckets. With multiple workers or hosts, the
effective quota is multiplied by the number of independent instances. When the key set reaches
`max_keys`, the least recently used key is evicted so a new key can be retained. High-cardinality
key churn can therefore reset older clients' local history; this middleware is not a robust
deployment-wide abuse barrier. Use an ingress/gateway policy or a separately installed shared
limiter for quotas that must span workers or hosts.

## Response behavior

The middleware consumes one token before route dispatch. Successful and rejected responses include
`X-RateLimit-Limit` and `X-RateLimit-Remaining`; it replaces any values with those names already on
the response. Rejections return HTTP 429 with JSON code `security.rate-limited` and a numeric
`retry_after`, plus an integer `Retry-After` header rounded up to at least one second. It preserves
other response headers and bodies. Tokens are not refunded when downstream work fails or is
cancelled.

## Operations

The `limiter` property exposes the local `RateLimiter` for inspecting `key_count` and explicitly
resetting one key. Avoid putting raw identities, API keys, or personal data in keys if they could be
exposed through debugging or process inspection. Hash or otherwise minimize retained identifiers
according to the application's privacy requirements.

Monitor 429 rates at the application or ingress layer. Tune policy based on legitimate traffic and
the number of ASGI workers. The limiter does not provide persistence, shared quotas, user identity,
authorization, WAF behavior, or upstream denial-of-service protection.
