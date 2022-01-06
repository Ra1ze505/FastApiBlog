from typing import List

from fastapi import APIRouter, Depends

from microblog.schemas import PostList, PostCreate, PostSingle
from microblog.service import create_post, get_all_posts
from user.auth import get_current_user
from user.schemas import UserInDB

router = APIRouter()


@router.get('/', response_model=List[PostList])
async def home():
    posts = await get_all_posts()
    print(posts[0])
    return posts


@router.post('/add', status_code=201, response_model=PostSingle)
async def add_post(item: PostCreate, user: UserInDB = Depends(get_current_user)):
    post = await create_post(item, user)
    return post
