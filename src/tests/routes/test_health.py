import pytest

pytestmark = pytest.mark.anyio


async def test_health_check(client):
    resp = client.get("/health/v1")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
