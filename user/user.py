from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from user.models import User
from user.schemas import UserView, UserRegister, Token
from user.service import create_user
from user.auth import get_current_user, authenticate_user, get_username_refresh_token, get_access_refresh_token

router = APIRouter()


@router.get('', response_model=UserView)
async def view(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/register', response_model=UserView)
async def register(user: UserRegister):
    result = await create_user(user)
    return result


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    access_token, refresh_token = await get_access_refresh_token(user.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post('/refresh', response_model=Token)
async def refresh(refresh_token: str):
    username = await get_username_refresh_token(refresh_token)
    access_token, refresh_token = await get_access_refresh_token(username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



