import sys
from typing import List

from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker, scoped_session

sys.path = ['', '..'] + sys.path[1:]

from core.db import engine
from models import Post
from schemas import PostCreate, PostList, PostView

app = FastAPI()

session = sessionmaker(bind=engine)
current_session = scoped_session(session)


@app.get('/', response_model=List[PostView])
async def home():
    posts = current_session.query(Post).order_by(Post.id).all()
    return posts


@app.post('/add', response_model=PostList)
async def add_post(item: PostCreate):
    post = Post(**item.dict())
    current_session.add(post)
    current_session.commit()
    return {**item.dict(), 'id': post.id}
