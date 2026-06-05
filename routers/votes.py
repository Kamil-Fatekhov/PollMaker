import fastapi
from fastapi import APIRouter, status

from database import SessionDep
from schemas.vote import SVoteCreate, SVoteResponse
from services.vote_service import create_vote

router = APIRouter()

@router.post("/polls/{poll_id}/vote", status_code=status.HTTP_201_CREATED, tags=["Голоса"], description="Создание голоса")
def add_vote(session: SessionDep, poll_id: int, user_id: int, payload: SVoteCreate) -> SVoteResponse:
    new_vote = create_vote(payload, poll_id, user_id, session)
    if new_vote is None:
        raise fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Что-то пошло не так")
    return SVoteResponse.model_validate(new_vote)