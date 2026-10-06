# orbit-security security

The HTTP limiter is one layer of defense. It does not identify users, authorize actions, or
coordinate quotas across processes. Keep trusted proxy configuration explicit and avoid using
untrusted request headers as limiter keys.

Authentication and authorization mechanisms are maintained by `orbit-auth`. Applications should
compose rate limiting with authenticated identity only through a trusted, explicit key function.
Do not log sensitive identity or tenant keys; hash or otherwise minimize retained identifiers when
the deployment's privacy policy requires it.
