# Orbit Security: security

`orbit-security` currently provides an opt-in in-process HTTP rate limiter. It is one resource
control and does not identify callers, authenticate credentials, authorize actions, or coordinate
quotas across processes.

## Trust boundaries

- By default, the limiter keys on `request.client_host`. Core must be configured with the trusted
  proxy policy for the deployment topology; forwarded headers from untrusted peers must not be
  treated as authoritative.
- A custom key function should use a trusted principal or tenant context produced by an
  authentication layer such as `orbit-auth`. Never use an unvalidated request header as proof of
  identity or tenancy.
- Keep keys free of credentials and minimize personal data. The limiter retains up to `max_keys`
  keys in process memory until eviction or reset.
- Rate limits apply independently per middleware instance. Do not treat local counters as global
  quotas or as a denial-of-service defense at the network edge.

## Request behavior

Each request consumes a token before downstream dispatch. Rejected requests receive HTTP 429 and
`Retry-After`; downstream failures and cancellation do not refund consumed tokens. The local LRU
evicts the least recently used key at capacity, so adversarial high-cardinality traffic can displace
existing buckets. Use gateway controls and network-level protections for abuse cases that require a
stronger boundary.

The middleware overwrites `X-RateLimit-Limit` and `X-RateLimit-Remaining` on the response. It keeps
other response headers intact. If middleware order affects a response or error handler, verify the
actual `ASGIApplication` stack in integration tests.

## Disclosure

For security vulnerabilities, follow the repository [security policy](../../SECURITY.md). Avoid
posting unpatched details in public issues.
