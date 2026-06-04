from models.user import UsersModel
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