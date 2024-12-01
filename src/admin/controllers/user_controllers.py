from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.schemas.auth_schemas import UserCreate, UserUpdate, UserRead
from src.services.user_service import UserService
from src.utils.dependencies import UOWDep
from src.logger import get_logger

router = APIRouter(tags=['admin/user'])
logger = get_logger(__name__)


@router.post("/user/add")
async def create_user(uow: UOWDep, user: UserCreate):
    try:
        result = await UserService().add_user(uow, user)
        logger.info("create_user successful")
        return result
    except Exception as e:
        logger.error("create_user failed", user_id=user.email, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/get/user/tg/{tg_id}")
async def get_user_by_tg(uow: UOWDep, tg_id: int):
    try:
        result = await UserService().get_user(uow, tg_id=tg_id)
        logger.info("get_user_by_tg successful")
        return result
    except Exception as e:
        logger.error("get_userby_tg failed", user_id=tg_id)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))
    

@router.get("/get/user/email/{email}")
async def get_user_by_email(uow: UOWDep, email: str):
    try:
        result = await UserService().get_user(uow, email=email)
        logger.info("get_user_by_email successful")
        return result
    except Exception as e:
        logger.error("get_user_by_email failed", user_id=email, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/users/", response_model=list[UserRead])
async def list_users(uow: UOWDep):
    try:
        result = await UserService().get_users(uow)
        logger.info("list_users successful")
        return result
    except Exception as e:
        logger.error("list_users failed", exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/update/user/{user_id}")
async def update_user(uow: UOWDep, user_id: str, user: dict):
    try:
        result = await UserService().edit_user(uow, user, user_id)
        logger.info("update_users successful")
        return result
    except Exception as e:
        logger.error("update_user failed", user_id=user_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/delete/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(uow: UOWDep, user_id: str):
    try:
        result = await UserService().remove_user(uow, user_id)
        logger.info("delete_user successful")
        return result
    except Exception as e:
        logger.error("delete_user failed", user_id=user_id, exc_info=e)
        return HTTPException(HTTP_400_BAD_REQUEST, str(e))
