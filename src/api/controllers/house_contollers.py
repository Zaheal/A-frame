from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from ...services.house_service import HouseService
from ...utils.dependencies import UOWDep
from ...schemas.base_schemas import SHouseRead

router = APIRouter(tags=["home"])


@router.get("/")
async def homepage():
    pass


@router.get("/{house_id}", response_model=SHouseRead)
async def get_selected_house(uow: UOWDep, house_id: int):
    try:
        return await HouseService().get_house(uow, house_id)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)





