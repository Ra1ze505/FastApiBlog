from sqlalchemy import select

from core.db import database
from microblog.models import posts
from microblog.schemas import PostCreate
from user.models import users
from user.schemas import UserInDB


async def create_post(item: PostCreate, user: UserInDB):
    post = posts.insert().values(**item.dict(), user=user.id)
    pk = await database.execute(post)
    return {**item.dict(), "id": pk, "user": {"id": user.id, "username": user.username}}


async def get_all_posts():
    u = users.alias('user')
    p = posts.alias('post')
    q = select([u.c.id.label("userId"), u.c.username.label("userName"), p]) \
        .select_from(p.join(u))
    post_list = await database.fetch_all(query=q)
    return [{**post, "user": {"id": post.get("userId"), "username": post.get("userName")}} for post in post_list]
