import uuid

from fastapi import APIRouter, HTTPException, Response, Cookie
from starlette.status import HTTP_400_BAD_REQUEST

from src.services.house_service import HouseService
from src.utils.dependencies import UOWDep
from src.schemas.base_schemas import SHouseRead

router = APIRouter(tags=["home"])


@router.get("/home")
async def set_user_id_in_cookie(
        response: Response,
        user_id: str | None = Cookie(default=None)
        ):
    """
    В Cookies записывается uuid пользователя, если его ещё нет

    :param user_id:
    :param response:
    """
    try:
        if user_id is None:
            user_id = uuid.uuid4()
            response.set_cookie(key="user_id", value=user_id)
        return None
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.get("/house/{house_id}", response_model=SHouseRead)
async def get_selected_house(
        uow: UOWDep,
        house_id: int
        ):
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
