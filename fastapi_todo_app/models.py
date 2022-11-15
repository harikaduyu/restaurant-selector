
from sqlalchemy import Boolean, Column, Integer, String
from fastapi_todo_app.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    complete = Column(Boolean, default=False)
