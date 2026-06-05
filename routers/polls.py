import fastapi
from fastapi import APIRouter, status

from database import SessionDep
from schemas.poll import SPollCreate, SPollResponse
from services.poll_service import poll_create, get_polls, get_poll, close_poll, delete_poll

router = APIRouter()


@router.post("/polls", status_code=status.HTTP_201_CREATED, tags=["Опросы"], description="Пользователь создает опрос")
def add_poll(poll: SPollCreate, session: SessionDep, user_id: int) -> SPollResponse:
    data = poll_create(session, poll, user_id)
    new_poll = SPollResponse.model_validate(data)
    return new_poll


@router.get("/polls", tags=["Опросы"], description="Получить список опросов")
def read_polls(session: SessionDep) -> list[SPollResponse]:
    polls = get_polls(session)
    return [SPollResponse.model_validate(poll) for poll in polls]


@router.get("/polls/{poll_id}", tags=["Опросы"], description="Получить опрос по айди")
def read_poll_by_id(session: SessionDep, poll_id: int) -> SPollResponse:
    poll = get_poll(session, poll_id)
    if poll:
        return SPollResponse.model_validate(poll)
    raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого опроса нет")

@router.patch("/polls/{poll_id}/close", tags=["Опросы"], description="Закрыть опрос")
def close(poll_id: int, user_id: int, session: SessionDep) -> SPollResponse:
    new_poll = close_poll(session, poll_id, user_id)
    if new_poll:
        return SPollResponse.model_validate(new_poll)
    raise fastapi.HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Отказано")

@router.delete("/polls/{poll_id}/delete", tags=["Опросы"], description="Удалить опрос", status_code=status.HTTP_204_NO_CONTENT)
def delete(poll_id: int, user_id: int, session: SessionDep):
    is_deleted = delete_poll(session, poll_id, user_id)
    if is_deleted is None:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Опрос не найден")
    if not is_deleted:
        raise fastapi.HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав")
    return