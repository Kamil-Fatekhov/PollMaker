from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base

class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("user_id", "poll_id"), )
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    option_index: Mapped[int]
    created_at: Mapped[datetime]
    user: Mapped["User"] = relationship(back_populates="votes")
    poll: Mapped["Poll"] = relationship(back_populates="votes")
