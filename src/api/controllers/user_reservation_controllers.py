from datetime import date

from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from fastapi_cache.decorator import cache

from src.schemas.base_schemas import SReservationRead, SReservationAdd, STemporaryReservationAdd
from src.services.reservation_service import ReservationService
from src.services.temporary_reservation_service import TemporaryReservationService
from src.utils.dependencies import UOWDep
from src.auth.user import current_active_user
from src.models.core_models import User
from src.logger import get_logger
from src.config.auth.strategy import get_jwt_strategy
from src.config.bot_config import get_config_bot

from tg_bot.bot import bot

router = APIRouter(tags=['choose'])
logger = get_logger(__name__)
strategy = get_jwt_strategy()
bot_settings = get_config_bot()

@router.get("/reservations/{house_id}", response_model=list[SReservationRead])
async def get_house_reservations(uow: UOWDep,
                                 house_id: int
                                 ) -> list[SReservationRead] | None:
    """
    Возвращает список дат, когда домик забронирован

    :param uow:
    :param house_id:
    :return:
    """
    try:
        result = await ReservationService().get_reservations(uow, house_id=house_id)
        logger.debug("get_house_reservations successful")
        return result
    except Exception as e:
        logger.error(f"get_house_reservation failed {house_id}", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, e)


@router.get("/my/reservations")
@cache(expire=60)
async def get_user_reservations(uow: UOWDep,
                                user: User = Depends(current_active_user)
                                ) -> list[SReservationRead] | None:
    """
    Возвращает список броней пользователя

    :param uow:
    :param user_id:
    """
    try:
        result = await ReservationService().get_reservations(uow, user_id=user.id)
        logger.debug("get_user_reservations successful")
        return result
    except Exception as e:
        logger.error(f"get_user_reservations failed {user.email}", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, e)



@router.post("/create/reservation")
async def create_reservation(uow: UOWDep,
                             reservation: SReservationAdd,
                             user: User = Depends(current_active_user)
                             ):
    """
    Создаёт бронь


    :param user:
    :param uow:
    :param reservation:
    :return:
    """
    try:
        result = await ReservationService().add_reservation(uow, reservation, user.id)
        logger.debug("create_reservation successful verify user")

        user_json = user.to_dict()
        reservation_json = SReservationAdd.model_validate(result)
        answer = f'!!!Бронь!!!\nИмя - {user_json['name']}, почта - {user_json['email']}, номер - {user_json['number']} \nэтот крутой перец забронировал домик №{reservation_json.house_id}, \n{reservation_json.start} - {reservation_json.end}, на сумму {reservation_json.full_price}₽ {"с допом" if reservation_json.add else "без допа"}'
        
        for admin in bot_settings.ADMIN_ID.split(','):
            await bot.send_message(admin, answer)
        return result
    except Exception as e:
        logger.error(f"create_reservation failed, {user.email}", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, e)


@router.post("/delete/reservation/{reservation_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_reservation(uow: UOWDep,
                             reservation_id: int,
                             user: User = Depends(current_active_user)
                             ) -> None:
    """
    Удаляет бронь

    :param user_id:
    :param uow:
    :param reservation_id:
    :return:
    """
    try:
        result = await ReservationService().remove_reservation(uow, reservation_id, user.id)
        logger.debug("delete_reservation successful")

        user_json = user.to_dict()
        reservation_json = SReservationAdd.model_validate(result)
        answer = f'Имя - {user_json['name']}, почта - {user_json['email']}, номер - {user_json['number']} \nэтот не крутой перец отменил бронь №{reservation_json.house_id}, \n{reservation_json.start} - {reservation_json.end}, на сумму {reservation_json.full_price}₽'
        if (reservation_json.start - date.today()).days > 7: 
            answer = "!!!Надо вернуть деньги!!!\n" + answer
        else: 
            answer = "!!!Отмена брони!!!\n" + answer

        for admin in bot_settings.ADMIN_ID.split(','):
            await bot.send_message(admin, answer)
        return result
    except Exception as e:
        logger.error(f"delete_reservation failed {user.email}", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.post("/create/temporary")
async def create_temporary_reservation(uow: UOWDep,
                                       temporary_reservation: STemporaryReservationAdd
                                       ):
    """
    Бронирование домика без регистрации
    
    :uow:
    :temporary_reservation:
    :return:
    """
    try:
        result = await TemporaryReservationService().add_temporary_reservation(uow, temporary_reservation)
        logger.debug("create_reservation successful not verify user")

        reservation_json = temporary_reservation.model_dump()
        answer = f'!!!Бронь!!!\nИмя - {reservation_json['name']}, почта - {reservation_json['email']}, номер - {reservation_json['number']} \nэтот крутой перец забронировал домик №{reservation_json["house_id"]}, \n{reservation_json["start"]} - {reservation_json["end"]}, на сумму {reservation_json["full_price"]}₽ {"с допом" if reservation_json["add"] else "без допа"}'
        
        for admin in bot_settings.ADMIN_ID.split(','):
            await bot.send_message(admin, answer)
        return result
    except Exception as e:
        logger.error(f"create_temprorary_reservation failed, {reservation_json['name']}: {reservation_json['email']}", exc_info=e)
        raise HTTPException(HTTP_400_BAD_REQUEST, e)
