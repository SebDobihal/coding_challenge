from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    description: str
    due_date: Optional[datetime] = Field(alias="due-date")
    done: Optional[bool]
    priority: Optional[int]

    class Config:
        from_attributes = True


class Todo(TodoCreate):
    id: int
