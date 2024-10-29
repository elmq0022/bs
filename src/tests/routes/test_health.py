import pytest

pytestmark = pytest.mark.anyio


async def test_health_check(client):
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
