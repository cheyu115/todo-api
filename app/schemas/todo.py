from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    is_completed: bool = False


class TodoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    is_completed: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    is_completed: Optional[bool] = None


class TodoResponse(TodoBase):
    id: str
    created_at: datetime
    updated_at: datetime
