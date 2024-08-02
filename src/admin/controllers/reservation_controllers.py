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


@router.post("/busy_time/add", dependencies=[Depends(current_superuser)])
async def create_busy_time(uow: UOWDep, busy_time: SReservationAdd):
    try:
        return await ReservationService().add_busy_time(uow, busy_time)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/busy_times/", response_model=list[SReservationRead], dependencies=[Depends(current_superuser)])
async def list_busy_times(uow: UOWDep):
    try:
        return await ReservationService().get_busy_times(uow)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/busy_time/{busy_time_id}", dependencies=[Depends(current_superuser)])
async def update_busy_time(uow: UOWDep, busy_time_id: int, busy_time: SReservationEdit):
    try:
        return await ReservationService().edit_busy_time(uow, busy_time, busy_time_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/busy_time/{busy_time_id}", status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(current_superuser)])
async def delete_busy_time(uow: UOWDep, busy_time_id: int):
    try:
        return await ReservationService().remove_busy_time(uow, busy_time_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))
