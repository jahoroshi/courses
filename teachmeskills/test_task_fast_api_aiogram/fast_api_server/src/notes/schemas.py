from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr



class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: int

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    tags: Optional[List[str]] = []

class NoteUpdate(NoteBase):
    tags: Optional[List[str]] = []

class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = []
    owner_id: int

    class Config:
        from_attributes = True
