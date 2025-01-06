from datetime import datetime, timedelta
from typing import Annotated, Literal
from fastapi import HTTPException, Path, Request
from inertia import InertiaResponse
from pydantic import BaseModel, Field
from sqlmodel import func, select
from nanoid import generate
from icecream import ic
import arrow
from config.database import SessionDep
from config.views import InertiaDependency
from config.app import app
from config.settings import DAYS_STALE
from services.db import TaskDescription, TaskItem


class AddDescription(BaseModel):
    slug: str = Field(min_length=1)
    content: str = Field(min_length=1)


class SlugTask(BaseModel):
    slug: str = Field(min_length=1)


class StatusTask(BaseModel):
    status: str = Field(min_length=1)
    slug: str = Field(min_length=1)


class CreateTask(BaseModel):
    name: str = Field(min_length=1)
    message: str = Field(min_length=1)


class TitleTask(BaseModel):
    title: str = Field(min_length=1)
    slug: str = Field(min_length=1)


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
    stale_limit = datetime.now() - timedelta(days=DAYS_STALE)
    saved_tasks = session.exec(
        select(TaskItem).where(TaskItem.date_created > stale_limit)
    ).all()
    tasks = [
        {
            "status": t.status,
            "name": t.title,
            "slug": t.slug,
            "date": arrow.get(t.date_created).humanize(),
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
        {
            "id": f"{d.id or ""}",
            "content": d.message,
            "date": arrow.get(d.date_created).humanize(),
        }
        for d in task.descriptions
    ]
    metadata = {
        "slug": task.slug,
        "date": f"{task.date_created}",
        "title": task.title,
        "status": task.status,
    }
    return await inertia.render(
        "TaskPage", {"descriptions": descriptions[::-1], "task": metadata}
    )


@app.get("/task-list", response_model=None)
async def task_list(
    inertia: InertiaDependency,
    session: SessionDep,
    req: Request,
    days: int = 0,
    pagenum: int = 0,
    numperpage: int = 3,
):
    total_count = session.exec(select(func.count()).select_from(TaskItem)).one()
    if days == 0:
        stmt = select(TaskItem)
    else:
        stmt = select(TaskItem).where(
            TaskItem.date_created > datetime.now() - timedelta(days=days)
        )
    tasks = session.exec(stmt.offset(pagenum * numperpage).limit(numperpage)).all()
    rows = [
        {
            "title": t.title,
            "slug": t.slug,
            "status": (
                "stale"
                if t.date_created < datetime.now() - timedelta(days=DAYS_STALE)
                else t.status
            ),
            "date": arrow.get(t.date_created).humanize(),
            "details": [
                {
                    "message": d.message[:50] + ("" if len(d.message) < 50 else "..."),
                    "date": arrow.get(d.date_created).humanize(),
                }
                for d in t.descriptions
            ],
        }
        for t in tasks
    ]
    return await inertia.render(
        "TaskList",
        {
            "rows": rows,
            "url": req.url.path,
            "total": total_count // numperpage
            + (1 if total_count % numperpage != 0 else 0),
        },
    )


@app.post("/create-task", response_model=None)
async def create_task(tasks: CreateTask, session: SessionDep):
    ic(tasks)
    task = TaskItem(title=tasks.name, slug=generate())
    description = TaskDescription(message=tasks.message, task_id=task.slug)
    session.add(task)
    session.add(description)
    session.commit()


@app.patch("/change-status", response_model=None)
async def change_status(task: StatusTask, session: SessionDep):
    found_status = session.exec(
        select(TaskItem).where(TaskItem.slug == task.slug)
    ).one()
    ic(found_status)
    found_status.status = upgrade_status(found_status.status)
    session.add(found_status)
    session.commit()


@app.delete("/delete-task", response_model=None)
async def delete_task(task: SlugTask, session: SessionDep):
    found_task = session.exec(select(TaskItem).where(TaskItem.slug == task.slug)).one()
    ic(found_task)
    session.delete(found_task)
    session.commit()


@app.post("/create-description", response_model=None)
async def create_description(task: AddDescription, session: SessionDep):
    description = TaskDescription(message=task.content, task_id=task.slug)
    session.add(description)
    session.commit()


@app.put("/update-description", response_model=None)
async def update_description(description: AddDescription, session: SessionDep):
    # TODO: add slug to description potentially?
    found_des = session.get_one(TaskDescription, int(description.slug))
    found_des.message = description.content
    session.add(found_des)
    session.commit()


@app.patch("/change-title", response_model=None)
async def change_task_title(task: TitleTask, session: SessionDep):
    found_task = session.exec(select(TaskItem).where(TaskItem.slug == task.slug)).one()
    ic(found_task)
    found_task.title = task.title
    session.add(found_task)
    session.commit()
