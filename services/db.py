from typing import Literal
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, String


class TaskItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True)
    title: str
    status: Literal["completed", "progressing", "queued", "stale"] = Field(
        default="queued", sa_type=String
    )
    date_created: datetime = Field(default=datetime.now())
    descriptions: list["TaskDescription"] = Relationship(
        back_populates="task", cascade_delete=True
    )


class TaskDescription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task_id: str | None = Field(
        default=None, foreign_key="taskitem.slug", ondelete="CASCADE"
    )
    message: str
    date_created: datetime = Field(default=datetime.now())
    task: TaskItem | None = Relationship(back_populates="descriptions")
