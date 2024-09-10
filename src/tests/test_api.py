from cgitb import reset
from typing import Any

import pytest
from httpx import AsyncClient

json = {
  "style": "18_century",
  "color": "green",
  "air_conditioner": True,
  "place": 4,
  "size": 40,
  "cost": 6500,
  "location": "left_bottom",
  "bath": True
}


@pytest.mark.asyncio
async def test_api_home(
        client: AsyncClient,
):
    response = await client.get("api/home")
    assert response.status_code == 200
    assert response.cookies.get("user_id") is not None


# @pytest.mark.asyncio
# async def test_admin(
#         client: AsyncClient,
#         session,
# ):
#     response = await client.get(
#         "api/house/1"
#     )
#     assert response.status_code == 200

@pytest.mark.asyncio
async def test_admin(
        client,
        authenticated
):
    response = await client.get(
        "admin/houses"
    )
    assert response.status_code == 200
