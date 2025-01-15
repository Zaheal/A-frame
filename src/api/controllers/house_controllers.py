from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi_cache.decorator import cache

from src.services.house_service import HouseService
from src.utils.dependencies import UOWDep
from src.schemas.base_schemas import SHouseRead
from src.logger import get_logger

router = APIRouter(tags=["home"])
logger = get_logger(__name__)


@router.get("/house/{house_id}", response_model=SHouseRead)
@cache(expire=60)
async def get_selected_house(
        uow: UOWDep,
        house_id: int
        ):
    """
    Information about house

    :param uow:
    :param house_id:
    :return: 
    """
    try:
        result = await HouseService().get_house(uow, house_id)
        logger.debug("get_selected_house successful")
        return result
    except Exception as e:
        logger.error(f"get_selected_house failed, {house_id}", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, e)
