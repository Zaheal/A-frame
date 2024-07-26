from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from ...schemas.base_schemas import SBusyTimeRead, SBusyTimeAdd
from ...services.busy_time_service import BusyTimeService
from ...utils.dependencies import UOWDep

router = APIRouter(tags=['choose'])


@router.get("/reservation/{house_id}", response_model=list[SBusyTimeRead])
async def get_reservations(uow: UOWDep, house_id: int):
    try:
        return await BusyTimeService().get_busy_times(uow, house_id=house_id)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.post("/create/reservation")
async def create_reservation(uow: UOWDep, busy_time: SBusyTimeAdd):
    try:
        return await BusyTimeService().add_busy_time(uow, busy_time)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.delete("/delete/reservation", status_code=HTTP_204_NO_CONTENT)
async def delete_reservation(uow: UOWDep, busy_time_id: int):
    try:
        return await BusyTimeService().remove_busy_time(uow, busy_time_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))



