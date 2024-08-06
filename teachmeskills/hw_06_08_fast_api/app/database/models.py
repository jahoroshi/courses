from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class TaskORM(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]


user_event_association = Table(
    'user_event_association',
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("event_id", ForeignKey("events.id"), primary_key=True),

)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    is_admin: Mapped[bool] = mapped_column(Boolean)

    events: Mapped[Optional[List['Event']]] = relationship('Event',
                                                           secondary=user_event_association,
                                                           back_populates='users', lazy='select')


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    meeting_time: Mapped[datetime] = mapped_column(DateTime)
    description: Mapped[str | None] = mapped_column(String(150))
    users: Mapped[Optional[List['User']]] = relationship('User',
                                                         secondary=user_event_association,
                                                         back_populates='events', lazy='select')
