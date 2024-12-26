from datetime import datetime
from sqlmodel import Field, SQLModel
from nanoid import generate

hungry = "yes"


class TaskItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(default=generate(), index=True)
    title: str
    date_created: datetime = Field(default=datetime.now())


class TaskDescription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task_id: str | None = Field(default=None, foreign_key="taskitem.slug")
    message: str
    date_created: datetime = Field(default=datetime.now())
