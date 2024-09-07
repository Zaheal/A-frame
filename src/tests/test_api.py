from typing import Any

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_api_home(
        client: AsyncClient,
):
    response = await client.get("api/home")
    assert response.status_code == 200
    assert response.cookies.get("user_id") is not None


@pytest.mark.asyncio
async def test_api_house_id(
        client: AsyncClient,
        session: Any
):
    response = await client.get("api/house/1")
    assert response.status_code == 200
