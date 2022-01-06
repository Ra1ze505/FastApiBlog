from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from user.models import User
from user.schemas import UserView, UserRegister
from user.service import create_user
from user.auth import get_current_user, authenticate_user, create_access_token

router = APIRouter()


@router.get('', response_model=UserView)
async def view(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/register', response_model=UserView)
async def register(user: UserRegister):
    result = await create_user(user)
    return result


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # print(form_data)
    user = await authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": token, "token_type": "bearer"}
    # return {}


