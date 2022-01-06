from datetime import datetime

from fastapi.security import OAuth2PasswordRequestForm

from core.db import database
from user.models import users
from user.schemas import UserRegister


async def create_user(item: UserRegister):
    user = users.insert().values(**item.dict(exclude={'password1', 'password2'}),
                                 password=item.get_hash_password())
    pk = await database.execute(user)
    return {**item.dict(), "id": pk}


async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    return user


