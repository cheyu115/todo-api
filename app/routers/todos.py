from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas.todo import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter()

FAKE_DATA: List[TodoResponse] = []


@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(payload: TodoCreate) -> TodoResponse:
    item = TodoResponse(
        id=str(datetime.now().timestamp()),
        title=payload.title,
        description=payload.description,
        is_completed=payload.is_completed,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    FAKE_DATA.append(item)
    return item


@router.get("/")
async def list_todos() -> List[TodoResponse]:
    return FAKE_DATA


@router.get("/{tid}", response_model=TodoResponse)
async def retrieve_todo(tid: str) -> TodoResponse:
    for item in FAKE_DATA:
        if item.id == tid:
            return item
    raise HTTPException(status_code=404, detail="Todo not found")


@router.patch("/{tid}", response_model=TodoResponse)
async def update_todo(tid: str, payload: TodoUpdate) -> TodoResponse:
    for item in FAKE_DATA:
        if item.id == tid:
            data = payload.model_dump(exclude_unset=True)
            for k, v in data.items():
                setattr(item, k, v)
            item.updated_at = datetime.now()
            return item
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{tid}", status_code=204)
async def delete_todo(tid: str) -> None:
    for i, item in enumerate(FAKE_DATA):
        if item.id == tid:
            FAKE_DATA.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")
