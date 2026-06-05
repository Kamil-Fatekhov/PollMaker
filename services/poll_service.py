from sqlalchemy import select

from database import SessionDep
from schemas.poll import SPollCreate
from models.poll import Poll
from datetime import datetime

def poll_create(session: SessionDep, data: SPollCreate, user_id: int) -> Poll | None:
    poll = Poll(title=data.title, description=data.description, options=data.options, creator_id=user_id, created_at=datetime.now())
    session.add(poll)
    session.commit()
    session.refresh(poll)
    return poll

def get_polls(session: SessionDep) -> list[Poll]:
    query = select(Poll)
    res = session.execute(query)
    polls = res.scalars().all()
    return polls

def get_poll(session: SessionDep, poll_id: int) -> Poll | None:
    query = select(Poll).where(Poll.id == poll_id)
    result = session.execute(query)
    existing_poll = result.scalar_one_or_none()
    if existing_poll:
        return existing_poll
    return None

def close_poll(session: SessionDep, poll_id: int, user_id: int) -> Poll | None:
    query = select(Poll).where(Poll.id == poll_id)
    result = session.execute(query)
    existing_poll = result.scalar_one_or_none()
    if existing_poll and existing_poll.creator_id == user_id:
        existing_poll.is_closed = True
        session.commit()
        return existing_poll
    return None

def delete_poll(session: SessionDep, poll_id: int, user_id: int) -> bool | None:
    query = select(Poll).where(Poll.id == poll_id)
    result = session.execute(query)
    existing_poll = result.scalar_one_or_none()
    if existing_poll:
        if existing_poll.creator_id == user_id:
            session.delete(existing_poll)
            session.commit()
            return True
        return False
    return None