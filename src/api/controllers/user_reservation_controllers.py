from fastapi import APIRouter, HTTPException, Cookie, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.schemas.base_schemas import SReservationRead, SReservationAdd
from src.services.reservation_service import ReservationService
from src.utils.dependencies import UOWDep
from src.auth.user import current_active_user
from src.models.core_models import User
from src.language.ru_lang import Dictionary
from src.logger import get_logger

router = APIRouter(tags=['choose'])
logger = get_logger(__name__)


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
        result = await ReservationService().get_reservations(uow, house_id=house_id)
        logger.info("get_house_reservations successful")
        return result
    except Exception as e:
        logger.error("get_house_reservation failed", house_id=house_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.get("/my/reservations")
async def get_user_reservations(uow: UOWDep, user_id: str | None = Cookie(default=None)) -> list[SReservationRead] | None:
    """
    Возвращает список броней пользователя

    :param uow:
    :param user_id:
    """
    try:
        result = await ReservationService().get_reservations(uow, user_id=user_id)
        logger.info("get_user_reservations successful")
        return result
    except Exception as e:
        logger.error("get_user_reservations failed", user_id=user_id, exc_info=e)
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
                result = await ReservationService().add_reservation(uow, reservation, user_id)
                logger.info("create_reservation successful noneverify user")
                return result
            else:
                raise NameError(Dictionary["to_homepage"])
        else:
            result = await ReservationService().add_reservation(uow, reservation, user.id)
            logger.info("create_reservation successful verify user")
            return result
    except Exception as e:
        logger.error("create_reservation failed", exc_info=e)
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
        result = await ReservationService().remove_reservation(uow, reservation_id, user_id)
        logger.info("delete_reservation successful")
        return result
    except Exception as e:
        logger.error("delete_reservation failed", user_id=user_id, exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))



