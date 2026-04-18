from datetime import datetime
from typing import List

from fastapi import APIRouter

from ..schemas.todo import TodoResponse

router = APIRouter()

FAKE_DATA: List[TodoResponse] = [
    TodoResponse(
        id="1",
        title="Sample",
        description="A sample todo",
        is_completed=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


@router.get("/")
async def list_todos() -> List[TodoResponse]:
    return FAKE_DATA


@router.post("/")
async def create_todo() -> TodoResponse:
    return FAKE_DATA[0]
