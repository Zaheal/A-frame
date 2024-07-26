from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from ...models.auth_models import User
from ...schemas.base_schemas import SHouseAdd, SHouseEdit
from ...services.house_service import HouseService
from ...utils.dependencies import UOWDep

router = APIRouter(prefix='/admin', tags=['admin'])


def is_admin():
    return User(is_superuser=True)


@router.post("/house/add")
async def create_house(uow: UOWDep, house: SHouseAdd):
    try:
        return await HouseService().add_house(uow, house)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/houses/")
async def list_houses(uow: UOWDep):
    try:
        return await HouseService().get_houses(uow)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/house/{house_id}")
async def update_house(uow: UOWDep, house_id: int, house: SHouseEdit):
    try:
        return await HouseService().edit_house(uow, house, house_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/house/{house_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_house(uow: UOWDep, house_id: int):
    try:
        return await HouseService().remove_house(uow, house_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))
