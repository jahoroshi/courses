from datetime import datetime
from typing import Optional, List, Literal

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

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
                                                           back_populates='users', lazy='selectin')

    notifications: Mapped[Optional[List['Notification']]] = relationship('Notification', back_populates='user',
                                                                         lazy='selectin')


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    # name2: Mapped[str] = mapped_column(String(50), unique=True)
    meeting_time: Mapped[datetime] = mapped_column(DateTime)
    description: Mapped[str | None] = mapped_column(String(150))
    users: Mapped[Optional[List['User']]] = relationship('User',
                                                         secondary=user_event_association,
                                                         back_populates='events', lazy='selectin')
    notifications: Mapped[Optional[List['Notification']]] = relationship('Notification', back_populates='event',
                                                                         lazy='selectin')


class Notification(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_task_id: Mapped[str] = mapped_column(String(50), unique=True)
    second_task_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    first_notification: Mapped[datetime]
    second_notification: Mapped[Optional[datetime]]
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'))
    event: Mapped['Event'] = relationship('Event', back_populates='notifications')

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped['User'] = relationship('User', back_populates='notifications')
