from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from ...models.core_models import User
from ...schemas.auth_schemas import UserCreate, UserUpdate, UserRead
from ...services.user_service import UserService
from ...utils.dependencies import UOWDep
from ...auth.user import current_superuser

router = APIRouter(prefix='/admin', tags=['admin'])


def is_admin():
    return User(is_superuser=True)


@router.post("/user/add", dependencies=[Depends(current_superuser)])
async def create_user(uow: UOWDep, user: UserCreate):
    try:
        return await UserService().add_user(uow, user)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/users/", response_model=list[UserRead], dependencies=[Depends(current_superuser)])
async def list_users(uow: UOWDep):
    try:
        return await UserService().get_users(uow)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/user/{user_id}", dependencies=[Depends(current_superuser)])
async def update_user(uow: UOWDep, user_id: int, user: UserUpdate):
    try:
        return await UserService().edit_user(uow, user, user_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/user/{user_id}", status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(current_superuser)])
async def delete_user(uow: UOWDep, user_id: int):
    try:
        return await UserService().remove_user(uow, user_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))
