from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    slug: str
    content: str
    author: str = "Admin"
    tags: list[str] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[list[str]] = None

class PostResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    slug: str
    content: str
    author: str
    createdAt: str
    updatedAt: Optional[str] = None
    tags: list[str] = []

    class Config:
        populate_by_name = True
        from_attributes = True