from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from fastapi_cache.decorator import cache

from src.schemas.base_schemas import SReservationAdd, SReservationEdit
from src.services.reservation_service import ReservationService
from src.services.temporary_reservation_service import TemporaryReservationService
from src.utils.dependencies import UOWDep
from src.models.core_models import User
from src.auth.user import current_active_user
from src.logger import get_logger

router = APIRouter(tags=['admin/reservation'])
logger = get_logger(__name__)


@router.post("/reservation/add")
async def create_reservation(uow: UOWDep, reservation: SReservationAdd, user: User = Depends(current_active_user)):
    try:
        result = await ReservationService().add_reservation(uow, reservation, user.id)
        logger.debug("create_reservation successful")
        return result    
    except Exception as e:
        logger.error("create_reservation failed", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/reservations")
@cache(expire=60)
async def list_reservations(uow: UOWDep):
    try:
        reservations = await ReservationService().get_reservations(uow)
        temp_reservations = await TemporaryReservationService().get_reservations(uow)
        result = reservations + temp_reservations
        logger.debug("list_reservations successful")
        return result
    except Exception as e:
        logger.error("list_reservations failed", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.post("/update/reservation/{reservation_id}")
async def update_reservation(uow: UOWDep, reservation_id: int, reservation: SReservationEdit):
    try:
        result = await ReservationService().edit_reservation(uow, reservation, reservation_id)
        logger.debug("update_reservation successful")
        return result    
    except Exception as e:
        logger.error("update_reservation failed", reservation_id=reservation_id, exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.post("/delete/reservation/{reservation_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_reservation(uow: UOWDep, reservation_id: int):
    try:
        result = await ReservationService().remove_reservation(uow, reservation_id)
        logger.debug("delete_reservation successful")
        return result
    except Exception as e:
        logger.error(f"delete_reservation failed, {reservation_id}", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.post("/delete/temporary/{reservation_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_temporary(uow: UOWDep, reservation_id: int):
    try:
        result = await TemporaryReservationService().remove_temporary_reservation(uow, reservation_id)
        logger.debug("delete_temporary successful")
        return result
    except Exception as e:
        logger.error(f"delete_temporary failed, {reservation_id}", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))