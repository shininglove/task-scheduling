from datetime import datetime, timedelta
from typing import Annotated, Literal
from fastapi import HTTPException, Path
from inertia import InertiaResponse
from pydantic import BaseModel, Field
from sqlmodel import select
from nanoid import generate
from icecream import ic
from config.database import SessionDep
from config.views import InertiaDependency
from config.app import app
from services.db import TaskDescription, TaskItem


class AddDescription(BaseModel):
    slug: str = Field(min_length=1)
    content: str = Field(min_length=1)


class TaskSlug(BaseModel):
    slug: str = Field(min_length=1)


class TaskStatus(BaseModel):
    status: str = Field(min_length=1)
    slug: str = Field(min_length=1)


class TaskCreate(BaseModel):
    name: str = Field(min_length=1)
    message: str = Field(min_length=1)


type Status = Literal["queued", "progressing", "completed", "stale"]


def upgrade_status(status: Status) -> Status:
    statuses: list[Status] = [
        "queued",
        "progressing",
        "completed",
        "stale",
    ]
    size = len(statuses) - 1
    position = statuses.index(status) + 1
    idx = position % size
    return statuses[idx]


@app.get("/", response_model=None)
async def index(inertia: InertiaDependency, session: SessionDep) -> InertiaResponse:
    stale_limit = datetime.now() - timedelta(days=5)
    saved_tasks = session.exec(
        select(TaskItem).where(TaskItem.date_created > stale_limit)
    ).all()
    tasks = [
        {
            "status": (
                "stale"
                if t.date_created < datetime.now() - timedelta(days=5)
                else t.status
            ),
            "name": t.title,
            "slug": t.slug,
            "date": f"{t.date_created}",
        }
        for t in saved_tasks
    ]
    return await inertia.render("Index", {"data": tasks})


@app.get("/task/{slug}", response_model=None)
async def task_page(
    slug: Annotated[str, Path(title="slug of the task")],
    inertia: InertiaDependency,
    session: SessionDep,
) -> InertiaResponse:
    task = session.exec(select(TaskItem).where(TaskItem.slug == slug)).one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task hasn't been created")
    descriptions = [
        {"content": d.message, "date": f"{d.date_created}"} for d in task.descriptions
    ]
    metadata = {
        "slug": task.slug,
        "date": f"{task.date_created}",
        "title": task.title,
        "status": (
            "stale"
            if task.date_created < datetime.now() - timedelta(days=5)
            else task.status
        ),
    }
    return await inertia.render(
        "TaskPage", {"descriptions": descriptions, "task": metadata}
    )


@app.post("/create-task", response_model=None)
async def create_task(tasks: TaskCreate, session: SessionDep):
    ic(tasks)
    task = TaskItem(title=tasks.name, slug=generate())
    description = TaskDescription(message=tasks.message, task_id=task.slug)
    session.add(task)
    session.add(description)
    session.commit()


@app.patch("/change-status", response_model=None)
async def change_status(task: TaskStatus, session: SessionDep):
    found_status = session.exec(
        select(TaskItem).where(TaskItem.slug == task.slug)
    ).one()
    ic(found_status)
    found_status.status = upgrade_status(found_status.status)
    session.add(found_status)
    session.commit()


@app.delete("/delete-task", response_model=None)
async def delete_task(task: TaskSlug, session: SessionDep):
    found_task = session.exec(select(TaskItem).where(TaskItem.slug == task.slug)).one()
    ic(found_task)
    session.delete(found_task)
    session.commit()


@app.post("/create-description", response_model=None)
async def create_description(task: AddDescription, session: SessionDep):
    description = TaskDescription(message=task.content, task_id=task.slug)
    session.add(description)
    session.commit()
