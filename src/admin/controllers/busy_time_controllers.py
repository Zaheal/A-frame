from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from ...models.auth_models import User
from ...schemas.base_schemas import SBusyTimeAdd, SBusyTimeEdit, SBusyTimeRead
from ...services.busy_time_service import BusyTimeService
from ...utils.dependencies import UOWDep

router = APIRouter(prefix='/admin', tags=['admin'])


def is_admin():
    return User(is_superuser=True)


@router.post("/busy_time/add")
async def create_busy_time(uow: UOWDep, busy_time: SBusyTimeAdd):
    try:
        return await BusyTimeService().add_busy_time(uow, busy_time)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/busy_times/", response_model=list[SBusyTimeRead])
async def list_busy_times(uow: UOWDep):
    try:
        return await BusyTimeService().get_busy_times(uow)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/busy_time/{busy_time_id}")
async def update_busy_time(uow: UOWDep, busy_time_id: int, busy_time: SBusyTimeEdit):
    try:
        return await BusyTimeService().edit_busy_time(uow, busy_time, busy_time_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/busy_time/{busy_time_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_busy_time(uow: UOWDep, busy_time_id: int):
    try:
        return await BusyTimeService().remove_busy_time(uow, busy_time_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))
