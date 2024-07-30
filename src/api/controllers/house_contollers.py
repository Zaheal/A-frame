import uuid

from fastapi import APIRouter, HTTPException, Response, Cookie
from starlette.status import HTTP_400_BAD_REQUEST

from ...services.house_service import HouseService
from ...utils.dependencies import UOWDep
from ...schemas.base_schemas import SHouseRead

router = APIRouter(tags=["home"])


@router.get("/")
async def homepage(response: Response, user_id: str | None = Cookie(default=None)):
    """
    Домашняя страница, в Cookies записывается uuid пользователя, если его ещё нет

    :param user_id:
    :param response:
    """
    if user_id:
        return None
    else:
        user_id = uuid.uuid4()
        response.set_cookie(key="user_id", value=user_id)


@router.get("/{house_id}", response_model=SHouseRead)
async def get_selected_house(uow: UOWDep, house_id: int):
    """
    При выборе домика на homepage, показывает информацию о нём

    :param uow:
    :param house_id:
    :return:
    """
    try:
        return await HouseService().get_house(uow, house_id)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)
