import uuid

from passlib.context import CryptContext
from pydantic import BaseModel, validator, EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    email: EmailStr


class UserRegister(User):
    password1: str
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    def get_hash_password(self):
        return pwd_context.hash(self.password1)


class UserView(User):
    id: int = None


class UserInDB(UserView):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class UserInPost(BaseModel):
    id: str
    username: str = None
