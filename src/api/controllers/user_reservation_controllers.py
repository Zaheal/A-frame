from fastapi import APIRouter, HTTPException, Cookie, Depends, Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from ...schemas.base_schemas import SReservationRead, SReservationAdd
from ...services.reservation_service import ReservationService
from ...utils.dependencies import UOWDep
from ...auth.user import current_active_user
from ...models.core_models import User

router = APIRouter(tags=['choose'])


@router.get("/reservations/{house_id}", response_model=list[SReservationRead])
async def get_house_reservations(uow: UOWDep, house_id: int) -> list[SReservationRead] | None:
    """
    Возвращает список дат, когда домик забронирован

    TODO избавиться от излишних запросов
    :param uow:
    :param house_id:
    :return:
    """
    try:
        return await ReservationService().get_reservations(uow, house_id=house_id)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.get("/my/reservations")
async def get_user_reservations(uow: UOWDep, user_id: str | None = Cookie(default=None)) -> list[SReservationRead] | None:
    """
    Возвращает список броней пользователя, хранящиеся в бд 30 дней

    TODO автоматически удалять бронь из бд после 30 дней окончания резервирования
    :param uow:
    :param user_id:
    """
    try:
        return await ReservationService().get_reservations(uow, user_id=user_id)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)



@router.post("/create/reservation")
async def create_reservation(uow: UOWDep,
                             reservation: SReservationAdd,
                             user_id: str | None = Cookie(default=None),
                             user: User | None = Depends(current_active_user)
                             ):
    """
    Создаёт бронь, если пользователь авторизирован получает данные из бд, а если нет,
    то запрашивает почту и берёт id пользователя из Cookie


    :param user:
    :param user_id:
    :param uow:
    :param reservation:
    :return:
    """
    try:
        if user is None:
            if user_id:
                return await ReservationService().add_reservation(uow, reservation, user_id)
            else:
                raise NameError("Прошу перейдите на главную страницу")
        else:
            return await ReservationService().add_reservation(uow, reservation, user.id)
    except Exception as e:
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.delete("/delete/reservation/{reservation_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_reservation(uow: UOWDep, reservation_id: int, user_id: str | None = Cookie(default=None)) -> None:
    """
    Удаляет бронь

    :param user_id:
    :param uow:
    :param reservation_id:
    :return:
    """
    try:
        return await ReservationService().remove_reservation(uow, reservation_id, user_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))



