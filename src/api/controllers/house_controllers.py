import uuid

from fastapi import APIRouter, HTTPException, Response, Cookie
from starlette.status import HTTP_400_BAD_REQUEST

from src.services.house_service import HouseService
from src.utils.dependencies import UOWDep
from src.schemas.base_schemas import SHouseRead
from src.logger import get_logger

router = APIRouter(tags=["home"])
logger = get_logger(__name__)


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
            response.set_cookie(key="user_id", value=user_id, httponly=True, path="/", samesite="lax")
        logger.info("set_user_id_in_cookie successful")
        return user_id
    except Exception as e:
        logger.error("set_user_id_in_cookie failed", exc_info=e)
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
        result = await HouseService().get_house(uow, house_id)
        logger.info("get_selected_house successful")
        return result
    except Exception as e:
        logger.error("get_selected_house failed", house_id=house_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, e)
