from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database import Base


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, index=True)
    due_date = Column(DateTime)
    done = Column(Boolean, default=False)
    priority = Column(Integer)
