from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str = ''
    text: str = ''


class PostParent(PostBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class PostList(PostBase):
    id: Optional[int]
    date: Optional[datetime]


class PostSingle(PostList):
    pass


class PostCreate(PostBase):
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True


class PostView(PostList):

    class Config:
        orm_mode = True
