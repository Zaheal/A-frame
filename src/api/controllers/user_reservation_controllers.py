from fastapi import APIRouter, HTTPException, Cookie
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from ...schemas.base_schemas import SBusyTimeRead, SBusyTimeAdd
from ...services.busy_time_service import BusyTimeService
from ...utils.dependencies import UOWDep

router = APIRouter(tags=['choose'])


@router.get("/reservations/{house_id}", response_model=list[SBusyTimeRead])
async def get_house_reservations(uow: UOWDep, house_id: int) -> list[SBusyTimeRead] | None:
    """
    Возвращает список дат, когда домик забронирован

    TODO избавиться от излишних запросов
    :param uow:
    :param house_id:
    :return:
    """
    try:
        return await BusyTimeService().get_busy_times(uow, house_id=house_id)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.get("/my/reservations")
async def get_user_reservations(uow: UOWDep, user_id: str | None = Cookie(default=None)) -> list[SBusyTimeRead] | None:
    """
    Возвращает список броней пользователя, хранящиеся в бд 30 дней

    TODO автоматически удалять бронь из бд после 30 дней окончания резервирования
    :param uow:
    :param user_id:
    """
    try:
        return await BusyTimeService().get_busy_times(uow, user_id=user_id)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)



@router.post("/create/reservation")
async def create_reservation(uow: UOWDep, busy_time: SBusyTimeAdd, user_id: str | None = Cookie(default=None)) -> int:
    """
    Создаёт бронь

    :param user_id:
    :param uow:
    :param busy_time:
    :return:
    """
    try:
        if user_id:
            request = await BusyTimeService().add_busy_time(uow, busy_time, user_id)
            return request
        else:
            raise NameError("Прошу перейдите на главную страницу")
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.delete("/delete/reservation/{busy_time_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_reservation(uow: UOWDep, busy_time_id: int, user_id: str | None = Cookie(default=None)) -> None:
    """
    Удаляет бронь

    :param user_id:
    :param uow:
    :param busy_time_id:
    :return:
    """
    try:
        return await BusyTimeService().remove_busy_time(uow, busy_time_id, user_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))



