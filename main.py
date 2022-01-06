from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from routes import routes
from core.db import database


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(routes)
