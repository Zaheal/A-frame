from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.schemas.auth_schemas import UserCreate, UserUpdate, UserRead
from src.services.user_service import UserService
from src.utils.dependencies import UOWDep
from src.auth.user import current_superuser
from src.logger import get_logger

router = APIRouter(tags=['admin/user'])
logger = get_logger(__name__)


@router.post("/user/add", dependencies=[Depends(current_superuser)])
async def create_user(uow: UOWDep, user: UserCreate):
    try:
        result = await UserService().add_user(uow, user)
        logger.info("create_user successful")
        return result
    except Exception as e:
        logger.error("create_user failed", user_id=user.email, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/get/user/")
async def get_user(uow: UOWDep, tg_id: int | None = None, email: str | None = None):
    try:
        result = await UserService().get_user(uow, tg_id=tg_id, email=email)
        logger.info("get_user successful")
        return result
    except Exception as e:
        logger.error("create_user failed", user_id=tg_id if tg_id else email, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/users/", response_model=list[UserRead], dependencies=[Depends(current_superuser)])
async def list_users(uow: UOWDep):
    try:
        result = await UserService().get_users(uow)
        logger.info("list_users successful")
        return result
    except Exception as e:
        logger.error("create_user failed", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/user/{user_id}", dependencies=[Depends(current_superuser)])
async def update_user(uow: UOWDep, user_id: int, user: UserUpdate):
    try:
        result = await UserService().edit_user(uow, user, user_id)
        logger.info("update_users successful")
        return result
    except Exception as e:
        logger.error("update_user failed", user_id=user_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/user/{user_id}", status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(current_superuser)])
async def delete_user(uow: UOWDep, user_id: int):
    try:
        result = await UserService().remove_user(uow, user_id)
        logger.info("delete_user successful")
        return result
    except Exception as e:
        logger.error("update_user failed", user_id=user_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))
