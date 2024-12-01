import re
from pwdlib.exceptions import UnknownHashError

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from fastapi_users import InvalidPasswordException

from src.language.ru_lang import Dictionary
from src.config.bot_config import get_config_bot
from src.logger import get_logger
from src.utils.pwd_validate import validate_password, verify_pwd

from tg_bot.states.state import LoginSignupState
from tg_bot.keyboards.kbs import email_confirm_kb, main_keyboard
from tg_bot.utils.utils import greet_user, UserActions, format_bool

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'

register_router = Router()

logger = get_logger(__name__)
settings = get_config_bot()

user_actions = UserActions()


@register_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду /start.
    """
    user, status = await user_actions.get_user_by_tg(message.from_user.id)
    logger.info(f"{status} cmd_start")
    is_new_user = 1 if "null" in user else 0
    
    await greet_user(message, is_new_user=is_new_user)


@register_router.callback_query(F.data.startswith("signup"))
async def cmd_signup(call: CallbackQuery, state: FSMContext):
    """
    Обрабатывает команду signup.
    """
    await call.message.answer("Напишите свою почту: ")
    await state.set_state(LoginSignupState.entering_email)


@register_router.message(lambda message: re.search(EMAIL_REGEX, message.text), LoginSignupState.entering_email)
async def search_email(message: Message, state: FSMContext):
    """
    Определяет есть ли пользователь с такой почтой или нет.
    """
    email = message.text
    try:
        user, status = await user_actions.get_user_by_email(email)
        await state.update_data(email=email)
        is_new_user = 1 if "null" in user else 0

        logger.info(f"{status} search_email")

        if is_new_user:
            await message.answer("Вы новый пользователь, придумайте пароль: ")
        else:
            await message.answer("Пользователь с такой почтой сущестует. Напишите ваш пароль: ")
        await state.set_state(LoginSignupState.entering_password)
    except Exception as e:
        logger.error("search_email", exc_info=e)
        await message.answer("Что-то пошло не так")


@register_router.message(LoginSignupState.entering_email)
async def error_email(message: Message, state: FSMContext):
    await message.reply("Это почта не действительна")
    await state.set_state(LoginSignupState.entering_email)


@register_router.message(LoginSignupState.entering_password)
async def set_password(message: Message, state: FSMContext):
    fsm_data = await state.get_data()
    user, status = await user_actions.get_user_by_email(fsm_data["email"])
    
    logger.info(f"{status} set_password")
    
    is_new_user = 1 if "null" in user else 0
    if is_new_user:
        try:
            verify = await validate_password(message.text, fsm_data["email"])
            user_data = {"email": fsm_data["email"], "password": message.text, "tg_id": message.from_user.id}
            user, status = await user_actions.create_user(user_data)

            logger.info(f"{status} set_password {is_new_user}")

            await message.answer(f"Вы в бд, {message.from_user.first_name}, хотите подтвердить свою почту? (рекомендую)",
                                reply_markup=email_confirm_kb())
        except InvalidPasswordException as e:
            logger.error(f"set_password {is_new_user}", exc_info=e)
            await message.reply("Ваш пароль должен быть больше 8 символов и не содержать в себе вашу почту.")        
    else:
        user = format_bool(user)
        user_data = eval(user)
        hashed_pwd = user_data["hashed_password"]
        try:
            verify = verify_pwd(message.text, hashed_pwd)
            if verify:
                user_data["tg_id"] = message.from_user.id
                user, status = await user_actions.update_user(user_data=user_data)

                logger.info(f"{status} set_password {is_new_user}")

                if user_data["is_verified"] is True:                
                    await message.answer("Ваш телеграм добавлен в базу данных, чем могу помочь?",
                                         reply_markup=main_keyboard())
                    await state.clear()
                else:
                    await message.answer("Почти усё закончилось, не хотите подтвердить свою почту?", reply_markup=email_confirm_kb())
            else:
                await message.reply("Неверный пароль, попробуйте ещё")

        except UnknownHashError as e:
            logger.error(f"set_password {is_new_user}", exc_info=e)
            await message.answer("какая то ошибка")


@register_router.callback_query(F.data.startswith("not_confirm_email"))
async def cmd_not_confirm(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("Хорошо, но вы не сможете забронировать дом без подтвержденной почты")


@register_router.callback_query(F.data.startswith("confirm_email"))
async def cmd_confirm_email(call: CallbackQuery, state: FSMContext):
    fsm_data = await state.get_data()
    email = fsm_data["email"]
    email_dict = {"email": email}
    status = await user_actions.confirm_email(email_dict)
    logger.info(f"cmd_confirm_email {status}")
    await call.message.answer("Проверьте свою почту, должна прийти ссылка с подтверждением")
    await state.clear()