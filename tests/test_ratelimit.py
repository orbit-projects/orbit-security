# Copyright 2026-present Orbit Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Integration tests for the separately installed HTTP rate-limit policy."""

import pytest
from orbit import Application, ApplicationConfig
from orbit.asgi import ASGIApplication, Request, Response
from orbit_testing import TestClient

from orbit_security import RateLimitMiddleware


@pytest.mark.asyncio
async def test_rate_limit_middleware_rejects_and_emits_headers() -> None:
    """Middleware throttles before route dispatch and reports standard limit headers."""
    app = Application(ApplicationConfig(name="rate-limit"))
    asgi = ASGIApplication(app)
    asgi.add_middleware(RateLimitMiddleware(1, 60, key=lambda request: "test-client"))
    invoked = 0

    @app.router.route("/", name="root")
    async def root(request: Request) -> Response:
        nonlocal invoked
        invoked += 1
        return Response(status=200, body=b"ok", headers=[("x-app", "preserved")])

    async with TestClient(asgi) as client:
        first = await client.request("GET", "/")
        second = await client.request("GET", "/")
    assert first.status == 200
    assert first.headers["x-ratelimit-limit"] == "1"
    assert first.headers["x-ratelimit-remaining"] == "0"
    assert first.headers["x-app"] == "preserved"
    assert second.status == 429
    assert second.headers["retry-after"] == "60"
    assert second.headers["x-ratelimit-remaining"] == "0"
    assert invoked == 1


def test_rate_limit_middleware_validates_key_callable() -> None:
    with pytest.raises(TypeError, match="callable"):
        RateLimitMiddleware(1, 1, key="client")  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_rate_limit_middleware_preserves_falsey_callable_key() -> None:
    class FalseyKey:
        def __bool__(self) -> bool:
            return False

        def __call__(self, request: Request) -> str:
            return "custom"

    middleware = RateLimitMiddleware(1, 1, key=FalseyKey())

    async def next_handler(request: Request) -> Response:
        return Response.text("ok")

    await middleware(Request("GET", "/"), next_handler)
    assert middleware.limiter.key_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(("limit", "period", "expected"), [(2, 1, "1"), (1, 1.0001, "2")])
async def test_retry_after_rounds_fractional_wait_up_to_a_whole_second(
    limit: int, period: float, expected: str
) -> None:
    middleware = RateLimitMiddleware(limit, period, key=lambda request: "client")

    async def next_handler(request: Request) -> Response:
        return Response.text("ok")

    for _ in range(limit):
        await middleware(Request("GET", "/"), next_handler)
    rejected = await middleware(Request("GET", "/"), next_handler)
    assert rejected.status == 429
    assert rejected.headers["retry-after"] == expected
