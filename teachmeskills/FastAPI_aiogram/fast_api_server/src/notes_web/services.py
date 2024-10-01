from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_302_FOUND
from starlette.templating import Jinja2Templates

from src.auth.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from database import get_session
from models import Note, Tag, User
from logger import logger  # Import logger for logging

templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["notes_web"])


# Endpoint to display all user notes
@router.get("/", response_class=HTMLResponse)
async def read_notes_web(
        request: Request,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    # Query to fetch notes along with tags for the current user
    result = await session.execute(
        select(Note)
        .where(Note.owner_id == current_user.id)
        .options(selectinload(Note.tags))
    )
    notes = result.scalars().all()
    logger.info(f"User {current_user.username} accessed their notes. Total notes: {len(notes)}")
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})


# Endpoint to display the form for creating a new note
@router.get("/notes-web/new", response_class=HTMLResponse)
async def create_note_form(request: Request):
    return templates.TemplateResponse("note_form.html", {"request": request})


# Endpoint to handle note creation from form submission
@router.post("/notes-web/new", response_class=HTMLResponse)
async def create_note_web(
        request: Request,
        title: str = Form(...),  # Title of the note from form
        content: str = Form(...),  # Content of the note from form
        tags: str = Form(""),  # Optional tags from form, comma-separated
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    # Create a new note object
    note = Note(
        title=title,
        content=content,
        owner_id=current_user.id,
    )
    # Handle tags: split and clean the input tags
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    if tag_list:
        for tag_name in tag_list:
            # Check if tag exists in the database
            result = await session.execute(
                select(Tag).where(Tag.name == tag_name)
            )
            db_tag = result.scalars().first()
            if not db_tag:
                db_tag = Tag(name=tag_name)
            note.tags.append(db_tag)  # Append tag to note
    session.add(note)
    await session.commit()
    await session.refresh(note)
    logger.info(f"User {current_user.username} created a new note: '{title}'")
    return templates.TemplateResponse("note_detail.html", {"request": request, "note": note})


# Endpoint to display the details of a specific note
@router.get("/notes-web/show/{note_id}", response_class=HTMLResponse)
async def read_note_web(
        request: Request,
        note_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user),
):
    # Query to fetch a specific note by ID
    result = await session.execute(
        select(Note)
        .where(Note.id == note_id, Note.owner_id == current_user.id)
        .options(selectinload(Note.tags))
    )
    note = result.scalars().first()
    if not note:
        logger.warning(f"Note with ID {note_id} not found for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Note not found")
    logger.info(f"User {current_user.username} accessed note: '{note.title}'")
    return templates.TemplateResponse("note_detail.html", {"request": request, "note": note})


# Endpoint to display the login form
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Endpoint to handle user login
@router.post("/login")
async def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),  # OAuth2 form data for username and password
        session: AsyncSession = Depends(get_session)
):
    # Authenticate user using provided credentials
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

    # Create access token with expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Redirect to home page after successful login
    response = RedirectResponse(url='/', status_code=HTTP_302_FOUND)
    # Set access token in cookies
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    logger.info(f"User {user.username} successfully logged in")
    return response
