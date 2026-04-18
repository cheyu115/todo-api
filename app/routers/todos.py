from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from schemas.todo import TodoResponse

router = APIRouter()

FAKE_DATA: List[TodoResponse] = []


@router.post("/")
async def create_todo(payload: TodoResponse) -> TodoResponse:
    payload.id = str(datetime.now().timestamp())
    FAKE_DATA.append(payload)
    return payload


@router.get("/")
async def list_todos() -> List[TodoResponse]:
    return FAKE_DATA


@router.get("/{tid}")
async def retrieve_todo(tid: str) -> TodoResponse:
    for item in FAKE_DATA:
        if item.id == tid:
            return item
    raise HTTPException(status_code=404, detail="Todo not found")


@router.patch("/{tid}")
async def update_todo(tid: str, payload: TodoResponse) -> TodoResponse:
    for item in FAKE_DATA:
        if item.id == tid:
            data = payload.model_dump(exclude_unset=True)
            for k, v in data.items():
                setattr(item, k, v)
            item.updated_at = datetime.now()
            return item
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{tid}")
async def delete_todo(tid: str) -> dict:
    for i, item in enumerate(FAKE_DATA):
        if item.id == tid:
            FAKE_DATA.pop(i)
            return {"detail": "deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
