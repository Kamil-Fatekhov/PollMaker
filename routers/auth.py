import fastapi

from database import SessionDep
from fastapi import APIRouter, status
from schemas.user import SUserCreate, SUserResponse, SUserLogin
from services.auth_service import register_user, authenticate_user, create_access_token
router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def user_register(user: SUserCreate, session: SessionDep) -> SUserResponse | None:
    data = register_user(session, user)
    if data:
        new_user = SUserResponse.model_validate(data)
        return new_user
    raise fastapi.HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже зарегистрирован")

@router.post("/login")
def login_user(user: SUserLogin, session:SessionDep):
    data = authenticate_user(session, user)
    if data:
        token = create_access_token(data.id)
        return {"access_token": token, "token_type": "bearer"}
    raise fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
