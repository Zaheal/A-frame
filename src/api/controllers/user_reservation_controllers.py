from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.schemas.base_schemas import SReservationRead, SReservationAdd
from src.services.reservation_service import ReservationService
from src.utils.dependencies import UOWDep
from src.auth.user import current_active_user
from src.models.core_models import User
from src.logger import get_logger
from src.config.auth.strategy import get_jwt_strategy

router = APIRouter(tags=['choose'])
logger = get_logger(__name__)
strategy = get_jwt_strategy()


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
async def get_user_reservations(uow: UOWDep, user: User = Depends(current_active_user)) -> list[SReservationRead] | None:
    """
    Возвращает список броней пользователя

    :param uow:
    :param user_id:
    """
    try:
        result = await ReservationService().get_reservations(uow, user_id=user.id)
        logger.info("get_user_reservations successful")
        return result
    except Exception as e:
        logger.error(f"get_user_reservations failed {user}", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, e)



@router.post("/create/reservation")
async def create_reservation(uow: UOWDep,
                             reservation: SReservationAdd,
                             user: User = Depends(current_active_user)
                             ):
    """
    Создаёт бронь, если пользователь авторизирован получает данные из бд


    :param user:
    :param uow:
    :param reservation:
    :return:
    """
    try:
        result = await ReservationService().add_reservation(uow, reservation, user.id)
        logger.info("create_reservation successful verify user")
        return result
    except Exception as e:
        logger.error("create_reservation failed", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, e)


@router.post("/delete/reservation/{reservation_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_reservation(uow: UOWDep, reservation_id: int, user: User = Depends(current_active_user)) -> None:
    """
    Удаляет бронь

    :param user_id:
    :param uow:
    :param reservation_id:
    :return:
    """
    try:
        result = await ReservationService().remove_reservation(uow, reservation_id, user.id)
        logger.info("delete_reservation successful")
        return result
    except Exception as e:
        logger.error(f"delete_reservation failed {user.email}", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))



