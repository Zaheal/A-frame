# from aiogram.filters import BaseFilter
# from aiogram.types import Message
#
# from src.client import check_user_in_db
#
#
# class UserExists(BaseFilter):
#     def __init__(self, user_exists: bool):
#         self.user_exists = user_exists
#
#     async def __call__(self, message: Message) -> bool:
#         user_id = message.from_user.id
#         user = await check_user_in_db(tg_id=user_id)
#
#         return user is not None if self.user_exists else user is None
