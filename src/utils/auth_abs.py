from abc import ABC, abstractmethod


class AuthAbstract(ABC):

    @abstractmethod
    async def login(self, **kwargs):
        ...


    @abstractmethod
    async def logout(self, **kwargs):
        ...

    
    @abstractmethod
    async def signup(self, **kwargs):
        ...


    @abstractmethod
    async def confirm_email(self, **kwargs):
        ...
    

    @abstractmethod
    async def forgot_password(self, **kwargs):
        ...
