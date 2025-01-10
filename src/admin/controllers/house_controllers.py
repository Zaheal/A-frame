from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.schemas.base_schemas import SHouseAdd, SHouseEdit
from src.services.house_service import HouseService
from src.utils.dependencies import UOWDep
from src.auth.user import current_superuser
from src.logger import get_logger

router = APIRouter(tags=['admin/house'])
logger = get_logger(__name__)


@router.post("/house/add", dependencies=[Depends(current_superuser)])
async def create_house(uow: UOWDep, house: SHouseAdd):
    try:
        result = await HouseService().add_house(uow, house)
        logger.debug("create_house successful")
        return result
    except Exception as e:
        logger.error("create_house failed", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/houses/", dependencies=[Depends(current_superuser)])
async def list_houses(uow: UOWDep):
    try:
        result = await HouseService().get_houses(uow)
        logger.debug("list_houses successful")
        return result
    except Exception as e:
        logger.error("list_houses failed", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/house/{house_id}", dependencies=[Depends(current_superuser)])
async def update_house(uow: UOWDep, house_id: int, house: SHouseEdit):
    try:
        result = await HouseService().edit_house(uow, house, house_id)
        logger.debug("update_house successful")
        return result
    except Exception as e:
        logger.error("update_house failed", house_id=house_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/house/{house_id}", status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(current_superuser)])
async def delete_house(uow: UOWDep, house_id: int):
    try:
        result = await HouseService().remove_house(uow, house_id)
        logger.debug("delete_house successful")
        return result
    except Exception as e:
        logger.error("delete_house failed", house_id=house_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))
