import datetime
import sys
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import models, schemas
from utils import crud

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# database dependency
def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return 'welcome to sipgate - todos list for the todo-list visit \todo'


@app.post("/todo", response_model=schemas.Todo, status_code=201)
async def create_todo(description: Annotated[str, Form()],
                      due_date: Annotated[datetime.datetime,
                      Form(alias="due-date")] = None,
                      priority: Annotated[int, Form()] = 0,
                      db: Session = Depends(get_db)):
    todo = schemas.TodoCreate
    todo.description = description
    todo.due_date = due_date
    todo.priority = priority
    todo.done = False
    json_dict: dict = await to_json_dict(crud.create_todo(db=db, todo=todo))
    return json_dict


@app.get("/todo", response_model=list[schemas.Todo])
async def read_todos(skip: int = 0, limit: int = sys.maxsize,
                     db: Session = Depends(get_db)):
    json_dict = jsonable_encoder(crud.get_todos(db, skip=skip, limit=limit))
    for todo in json_dict:
        replace_due_date(todo)
    return json_dict


@app.get("/todo/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = await check_todo_exists(db, todo_id)
    json_dict = await to_json_dict(db_todo)
    return json_dict


async def to_json_dict(db_todo):
    json_dict = jsonable_encoder(db_todo)
    replace_due_date(json_dict)
    return json_dict


def replace_due_date(json_todo):
    if json_todo:
        json_todo["due-date"] = json_todo.pop("due_date")


async def check_todo_exists(db, todo_id):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404,
                            detail="Todo with id {} not found".format(todo_id))
    return db_todo


@app.patch("/todo/{todo_id}", status_code=204)
async def update_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = await check_todo_exists(db, todo_id)
    crud.update_todo(db, db_todo)


@app.delete("/todo/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = await check_todo_exists(db, todo_id)
    crud.delete_todo(db, db_todo)
