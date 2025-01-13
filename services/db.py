from typing import Literal
from datetime import timezone, datetime
from sqlmodel import Field, Relationship, SQLModel, String
from nanoid import generate


class TaskItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(default_factory=generate,index=True)
    title: str
    status: Literal["completed", "progressing", "queued", "blocked"] = Field(
        default="queued", sa_type=String
    )
    date_created: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = Field(default=None, nullable=True)
    mailable: bool = Field(default=True)
    descriptions: list["TaskDescription"] = Relationship(
        back_populates="task", cascade_delete=True
    )


class TaskDescription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task_id: str | None = Field(
        default=None, foreign_key="taskitem.slug", ondelete="CASCADE"
    )
    message: str
    date_created: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = Field(default=None, nullable=True)
    mailable: bool = Field(default=True)
    task: TaskItem = Relationship(back_populates="descriptions")
