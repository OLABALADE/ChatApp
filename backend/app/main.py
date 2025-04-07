from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.controllers import users, chats, messages
from app.core.db import close_db_pool, init_db_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db_pool()
    yield
    close_db_pool()


app = FastAPI(title="Chat API", lifespan=lifespan)

app.include_router(users.router)
app.include_router(chats.router)
app.include_router(messages.router)


@app.get("/")
def home():
    return {"message": "Welcome to Chat App API"}
