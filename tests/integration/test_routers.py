import pytest

@pytest.mark.asyncio
async def test_create_item(client):
    response = await client.post("/items", json={"name": "Test"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test"
