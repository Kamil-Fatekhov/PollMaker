from sqlalchemy import select

from database import SessionDep
from models.poll import Poll
from models.user import User
from models.vote import Vote
from schemas.vote import SVoteCreate
from datetime import datetime


def create_vote(data: SVoteCreate, poll_id: int, user_id: int, session: SessionDep) -> Vote | None:
    query = select(Poll).where(Poll.id == poll_id)
    result = session.execute(query)
    existing_poll = result.scalar_one_or_none()
    if not existing_poll:
        return None
    if existing_poll.is_closed:
        return None
    if not 0 <= data.option_index < len(existing_poll.options):
        return None
    query = select(Vote).where(Vote.user_id == user_id, Vote.poll_id == poll_id)
    result = session.execute(query)
    existing_vote = result.scalar_one_or_none()
    if existing_vote:
        return None
    new_vote = Vote(option_index=data.option_index, poll_id=poll_id, user_id=user_id, created_at=datetime.now())
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)
    return new_vote
