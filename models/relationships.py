from sqlalchemy.orm import relationship
from models.user import User
from models.poll import Poll
from models.vote import Vote

User.polls = relationship("Poll", back_populates="creator", lazy="selectin")
User.votes = relationship("Vote", back_populates="user", lazy="selectin")

Poll.creator = relationship("User", back_populates="polls", lazy="selectin")
Poll.votes = relationship("Vote", back_populates="poll", lazy="selectin")

Vote.user = relationship("User", back_populates="votes", lazy="selectin")
Vote.poll = relationship("Poll", back_populates="votes", lazy="selectin")