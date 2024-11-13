import pytest


@pytest.mark.asyncio
async def test_health_check(test_client):
    response = test_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}
