import sys
from typing import Type

from sqlalchemy.orm import Session

from models import models, schemas
from models.models import Todo


def get_todo(db: Session, todo_id: int) -> Todo:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = sys.maxsize) \
        -> list[Type[Todo]]:
    return db.query(models.Todo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(description=todo.description,
                          due_date=todo.due_date, done=todo.done,
                          priority=todo.priority)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo: schemas.Todo):
    todo.done = True
    print("hey")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return get_todos(db, todo.id)


def delete_todo(db: Session, todo: schemas.Todo):
    db.delete(todo)
    db.commit()
