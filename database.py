from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Annotated
from fastapi import Depends
from config import DATABASE_URL
engine = create_engine(DATABASE_URL)
new_session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    with new_session() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]