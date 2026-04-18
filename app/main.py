from fastapi import FastAPI
from app.routers.todos import router as todos_router

app = FastAPI()

app.include_router(todos_router, prefix="/todos")


@app.get("/")
async def root():
    return {"message": "hello, world"}
