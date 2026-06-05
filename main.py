from routers import polls
from routers.auth import router as auth_router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base, engine
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Включение сервера")
    Base.metadata.create_all(bind=engine)

    yield
    print("Выключение сервера")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(polls.router)