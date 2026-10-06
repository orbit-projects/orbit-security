# ADR 0001: Cross-cutting security controls

- Status: Accepted
- Date: 2026-10-06

## Context

Identity and authentication capabilities need a focused package boundary. Request throttling is
useful to applications but is neither authentication nor authorization.

## Decision

Keep `orbit-security` focused on cross-cutting controls such as bounded HTTP rate limiting. Put
authenticators, identity/token contracts, OAuth/OIDC contracts, and role/policy authorization in
`orbit-auth` and its optional integrations.

## Consequences

- Installing `orbit-security` does not install an authenticator.
- The local rate limiter remains per process and per worker.
- Applications that need both capabilities install `orbit-auth` and `orbit-security` explicitly.
