from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from ...models.core_models import User
from ...schemas.base_schemas import SReservationAdd, SReservationEdit, SReservationRead
from ...services.reservation_service import ReservationService
from ...utils.dependencies import UOWDep
from ...auth.user import current_superuser

router = APIRouter(prefix='/admin', tags=['admin'])


def is_admin():
    return User(is_superuser=True)


@router.post("/reservation/add", dependencies=[Depends(current_superuser)])
async def create_reservation(uow: UOWDep, reservation: SReservationAdd):
    try:
        return await ReservationService().add_reservation(uow, reservation)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/reservations/", response_model=list[SReservationRead], dependencies=[Depends(current_superuser)])
async def list_reservations(uow: UOWDep):
    try:
        return await ReservationService().get_reservations(uow)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/reservation/{reservation_id}", dependencies=[Depends(current_superuser)])
async def update_reservation(uow: UOWDep, reservation_id: int, reservation: SReservationEdit):
    try:
        return await ReservationService().edit_reservation(uow, reservation, reservation_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/reservation/{reservation_id}", status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(current_superuser)])
async def delete_reservation(uow: UOWDep, reservation_id: int):
    try:
        return await ReservationService().remove_reservation(uow, reservation_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))
