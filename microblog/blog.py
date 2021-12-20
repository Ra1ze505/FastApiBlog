import sys
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

sys.path = ['', '..'] + sys.path[1:]

from core.db import engine
from models import Post
from schemas import PostCreate, PostList

app = FastAPI()

session = sessionmaker(bind=engine)
current_session = scoped_session(session)


@app.get('/')
def home():
    posts = current_session.query(Post).order_by(Post.id)
    print(posts.first().id)
    return {'hi': 'world'}


@app.post('/add', response_model=PostList)
def add_post(item: PostCreate):
    post = Post(**item.dict())
    current_session.add(post)
    current_session.commit()
    return {**item.dict(), 'id': post.id}

