from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.auth.auth import get_current_user
from database import get_session
from models import Note, Tag, User
from src.notes.schemas import NoteCreate, NoteRead, NoteUpdate
from logger import logger

router = APIRouter(tags=["notes"])

# Create a new note with optional tags
@router.post("/notes/", response_model=NoteRead, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def create_note(
    note: NoteCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id,
    )
    # Adding tags if provided
    if note.tags:
        for tag_name in note.tags:
            result = await session.execute(select(Tag).where(Tag.name == tag_name))
            db_tag = result.scalars().first()
            if not db_tag:
                db_tag = Tag(name=tag_name)
            db_note.tags.append(db_tag)
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    logger.info(f"Note '{db_note.title}' created by user {current_user.username}")
    return db_note

# Get all notes for the current user
@router.get("/notes/", response_model=List[NoteRead])
async def read_notes(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(Note)
        .where(Note.owner_id == current_user.id)
        .options(selectinload(Note.tags))
    )
    notes = result.scalars().all()
    logger.info(f"User {current_user.username} retrieved {len(notes)} notes")
    return notes

# Get a specific note by ID for the current user
@router.get("/notes/{note_id}", response_model=NoteRead)
async def read_note(
    note_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(Note)
        .where(Note.id == note_id, Note.owner_id == current_user.id)
        .options(selectinload(Note.tags))
    )
    note = result.scalars().first()
    if not note:
        logger.warning(f"Note with ID {note_id} not found for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Note not found")
    logger.info(f"User {current_user.username} retrieved note '{note.title}'")
    return note

# Update an existing note and its tags
@router.put("/notes/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(Note)
        .where(Note.id == note_id, Note.owner_id == current_user.id)
        .options(selectinload(Note.tags))
    )
    db_note = result.scalars().first()
    if not db_note:
        logger.warning(f"Note with ID {note_id} not found for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note_update.title
    db_note.content = note_update.content
    # Update tags if provided
    if note_update.tags is not None:
        db_note.tags.clear()
        for tag_name in note_update.tags:
            result = await session.execute(select(Tag).where(Tag.name == tag_name))
            db_tag = result.scalars().first()
            if not db_tag:
                db_tag = Tag(name=tag_name)
            db_note.tags.append(db_tag)
    await session.commit()
    await session.refresh(db_note)
    logger.info(f"Note '{db_note.title}' updated by user {current_user.username}")
    return db_note

# Delete a specific note
@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(Note).where(Note.id == note_id, Note.owner_id == current_user.id)
    )
    db_note = result.scalars().first()
    if not db_note:
        logger.warning(f"Note with ID {note_id} not found for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Note not found")
    await session.delete(db_note)
    await session.commit()
    logger.info(f"Note '{db_note.title}' deleted by user {current_user.username}")
    return {"message": "Note successfully deleted"}

# Search for notes by tag
@router.get("/notes/search/", response_model=List[NoteRead])
async def search_notes_by_tag(
    tag_name: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(Note)
        .join(Note.tags)
        .where(
            Tag.name == tag_name,
            Note.owner_id == current_user.id
        )
        .options(selectinload(Note.tags))
    )
    notes = result.scalars().all()
    logger.info(f"User {current_user.username} searched for notes with tag '{tag_name}' and found {len(notes)} notes")
    return notes
