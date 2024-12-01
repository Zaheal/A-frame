from aiogram.filters.state import State, StatesGroup


class LoginSignupState(StatesGroup):
    choosing_signup = State()
    entering_email = State()
    entering_password = State()
