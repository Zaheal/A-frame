from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.schemas.base_schemas import SReservationAdd, SReservationEdit
from src.services.reservation_service import ReservationService
from src.utils.dependencies import UOWDep
from src.auth.user import current_superuser
from src.logger import get_logger

router = APIRouter(tags=['admin/reservation'])
logger = get_logger(__name__)


@router.post("/reservation/add")
async def create_reservation(uow: UOWDep, reservation: SReservationAdd):
    try:
        result = await ReservationService().add_reservation(uow, reservation)
        logger.info("create_reservation successful")
        return result    
    except Exception as e:
        logger.error("create_reservation failed", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/reservations")
async def list_reservations(uow: UOWDep):
    try:
        result = await ReservationService().get_reservations(uow)
        logger.info("list_reservations successful")
        return result    
    except Exception as e:
        logger.error("list_reservations failed", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/reservation/{reservation_id}", dependencies=[Depends(current_superuser)])
async def update_reservation(uow: UOWDep, reservation_id: int, reservation: SReservationEdit):
    try:
        result = await ReservationService().edit_reservation(uow, reservation, reservation_id)
        logger.info("update_reservation successful")
        return result    
    except Exception as e:
        logger.error("update_reservation failed", reservation_id=reservation_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/reservation/{reservation_id}", status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(current_superuser)])
async def delete_reservation(uow: UOWDep, reservation_id: int):
    try:
        result = await ReservationService().remove_reservation(uow, reservation_id)
        logger.info("delete_reservation successful")
        return result    
    except Exception as e:
        logger.error("delete_reservation failed", reservation_id=reservation_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))
