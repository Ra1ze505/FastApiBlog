from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.utils import get_db
from microblog.models import Post
from microblog.schemas import PostList, PostView, PostCreate

router = APIRouter()


@router.get('/', response_model=List[PostView])
async def home(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.id).all()
    return posts


@router.post('/add', response_model=PostList)
async def add_post(item: PostCreate, db: Session = Depends(get_db)):
    post = Post(**item.dict())
    db.add(post)
    db.commit()
    return {**item.dict(), 'id': post.id}
