from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

# from ..filters.user_filter import UserExists
from ..lexicon.ru_lexicon import RU_LEXICON

router = Router()

# router.message.filter(UserExists(user_exists=True))


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(RU_LEXICON["start"])
