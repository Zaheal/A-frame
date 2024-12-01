from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from src.config.bot_config import get_config_bot
from src.language.ru_lang import Dictionary

settings = get_config_bot()


def start_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=Dictionary["sign_up_bot"], callback_data="signup")
    kb.adjust(1)
    return kb.as_markup()


def email_confirm_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Да, отправить подтверждение на почту", callback_data="confirm_email")
    kb.button(text="Нет", callback_data="not_confirm_email")
    kb.adjust(1)
    return kb.as_markup()


def main_keyboard(user_id: int, first_name: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    url_applications = f"{settings.BASE_SITE}/api/my/reservations"
    # url_add_application = f'{settings.BASE_SITE}/form?user_id={user_id}&first_name={first_name}'
    kb.button(text="🌐 Моя бронь", web_app=WebAppInfo(url=url_applications, ))
    # kb.button(text="📝 Забронировать", web_app=WebAppInfo(url=url_add_application))
    kb.button(text="ℹ️ О нас")
    if user_id in map(lambda x: int(x), settings.ADMIN_ID.split(",")):
        kb.button(text="🔑 Админ панель")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def back_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    url_applications = f"{settings.BASE_SITE}/admin?admin_id={user_id}"
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 На главную", callback_data="back_home")
    kb.button(text="📝 Смотреть заявки", web_app=WebAppInfo(url=url_applications))
    kb.adjust(1)
    return kb.as_markup()


def app_keyboard(user_id: int, first_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    url_add_application = f'{settings.BASE_SITE}/'
    kb.button(text="📝 Оставить заявку", web_app=WebAppInfo(url=url_add_application))
    kb.adjust(1)
    return kb.as_markup()
