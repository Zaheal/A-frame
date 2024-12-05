import httpx

from .auth_abs import AuthAbstract


class AuthMethods(AuthAbstract):

    async def login(self, email, password):
        