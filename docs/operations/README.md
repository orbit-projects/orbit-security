# orbit-security operations

Configure a finite limit, period, and key bound when constructing `RateLimitMiddleware`. The
default key is the validated client host. Behind a proxy, configure Core's trusted forwarded-header
policy or provide a key function that uses a trusted identity. Never trust arbitrary forwarding
headers.

The limiter is in-process and per worker. Size its `max_keys` for the expected active client set;
least-recently-used keys are evicted at capacity. Use a gateway or a dedicated distributed service
for deployment-wide abuse protection or quotas shared across hosts.
