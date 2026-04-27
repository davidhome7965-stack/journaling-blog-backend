from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        from pydantic.json_schema import JsonSchemaValue
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

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