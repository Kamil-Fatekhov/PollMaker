from __future__ import annotations
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime
class Poll(Base):
    __tablename__ = "polls"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime]
    is_closed: Mapped[bool] = mapped_column(default=False)
    options: Mapped[list[str]] = mapped_column(JSON, default=list)