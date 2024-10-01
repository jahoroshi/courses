# models.py

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Table,
    ForeignKey,
    Text,
    UniqueConstraint, BigInteger,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

note_tag_association = Table(
    'note_tag_association',
    Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
    UniqueConstraint('note_id', 'tag_id', name='uix_note_tag'),
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = relationship('Note', back_populates='owner')
    telegram_id = Column(BigInteger, unique=True, nullable=True)


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='notes')
    tags = relationship(
        'Tag',
        secondary=note_tag_association,
        back_populates='notes',
        lazy='joined',
    )

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    notes = relationship(
        'Note',
        secondary=note_tag_association,
        back_populates='tags',
    )
