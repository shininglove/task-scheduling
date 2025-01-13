from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal, Sequence
from fastapi import HTTPException, Path, Request
from fastapi.responses import FileResponse, HTMLResponse
from inertia import InertiaResponse
from pydantic import BaseModel, Field
from sqlmodel import func, select
from icecream import ic
import arrow
from config.database import SessionDep
from config.views import InertiaDependency, MAIL_TEMPLATE, public_dir
from config.app import app
from config.settings import DAYS_STALE
from services.db import TaskDescription, TaskItem
from services.report import mail_report


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


class Mailibility(BaseModel):
    flag: bool = Field()
    kind: Literal["task", "description"] = Field(min_length=1)
    slug: str = Field(min_length=1)


type Status = Literal["queued", "progressing", "completed", "blocked"]


def upgrade_status(status: Status) -> Status:
    statuses: list[Status] = [
        "queued",
        "progressing",
        "completed",
        "blocked",
    ]
    size = len(statuses)
    position = statuses.index(status) + 1
    idx = position % size
    return statuses[idx]


def format_status(status: Status) -> str:
    lookup = {
        "queued": "Queued",
        "progressing": "In-Progress",
        "completed": "Completed",
        "blocked": "Blocked",
    }
    return lookup[status]


def process_tasks(
    items: Sequence[TaskItem], time_limit: datetime, placeholder: str = ""
) -> str:
    html = ""
    for item in items:
        if item.mailable:
            header = f"<span><b>{item.title}</b> [{format_status(item.status)}]</span>"
            details = []
            for d in item.descriptions:
                if d.updated_at > time_limit and d.mailable:
                    details.append(f"<li>{d.message}</li>")
            points = f"<ul>{''.join(details)}</ul>"
            html += f"{header}{points}"
    return placeholder if len(items) == 0 else html


@app.get("/", response_model=None)
async def index(inertia: InertiaDependency, session: SessionDep) -> InertiaResponse:
    stale_limit = datetime.now() - timedelta(days=DAYS_STALE)
    saved_tasks = session.exec(
        select(TaskItem).where(TaskItem.updated_at > stale_limit)
    ).all()
    tasks = [
        {
            "status": t.status,
            "name": t.title,
            "slug": t.slug,
            "date": arrow.get(t.date_created).humanize(),
            "fulldate": arrow.get(t.date_created).format("MM-DD-YYYY")
        }
        for t in saved_tasks
    ]
    return await inertia.render("Index", {"data": tasks})


@app.get("/favicon.ico")
async def favicon() -> FileResponse:
    return FileResponse(public_dir / "favicon.ico")


@app.get("/settings", response_model=None)
async def settings(inertia: InertiaDependency) -> InertiaResponse:
    return await inertia.render("Settings", {})


@app.get("/mail-preview", response_model=None)
async def mail_preview(session: SessionDep):
    week_old = datetime.now() - timedelta(days=7)
    sendable_tasks = session.exec(
        select(TaskItem).where(TaskItem.updated_at > week_old)
    ).all()
    task_html = process_tasks(
        [t for t in sendable_tasks if t.status != "blocked"],
        week_old,
        "Nothing to report this week",
    )
    blocked_html = process_tasks(
        [s for s in sendable_tasks if s.status == "blocked"],
        week_old,
        "No blockers at this time",
    )
    with open(MAIL_TEMPLATE) as tem:
        html = tem.read()
        html = html.replace("$tasks", task_html)
        html = html.replace("$blockers", blocked_html)
    return HTMLResponse(content=html)


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
            "fulldate": arrow.get(d.date_created).format("MM-DD-YYYY")
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
    page: int = 1,
    perpage: int = 5,
):
    stmt = select(TaskItem)
    count_stmt = select(func.count()).select_from(TaskItem)
    if days != 0:
        stmt = stmt.where(TaskItem.updated_at > datetime.now() - timedelta(days=days))
        count_stmt = count_stmt.where(
            TaskItem.updated_at > datetime.now() - timedelta(days=days)
        )
    total_count = session.exec(count_stmt).one()
    tasks = session.exec(stmt.offset((page - 1) * perpage).limit(perpage)).all()
    message_size = 50
    rows = [
        {
            "title": t.title,
            "slug": t.slug,
            "status": t.status,
            "mailable": t.mailable,
            "date": arrow.get(t.date_created).humanize(),
            "fulldate": arrow.get(t.date_created).format("MM-DD-YYYY"),
            "details": [
                {
                    "message": d.message[:message_size]
                    + ("" if len(d.message) < message_size else "..."),
                    "date": arrow.get(d.date_created).humanize(),
                    "fulldate": arrow.get(d.date_created).format("MM-DD-YYYY"),
                    "slug": f"{d.id}",
                    "mailable": d.mailable,
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
            "total": total_count // perpage + (1 if total_count % perpage != 0 else 0),
        },
    )


@app.post("/send-report", response_model=None)
async def send_report(session: SessionDep):
    mail_report()


@app.post("/create-task", response_model=None)
async def create_task(tasks: CreateTask, session: SessionDep):
    # NOTE: need to sub out "'" because it breaks inertia
    ic(tasks)
    task = TaskItem(title=tasks.name.replace("'", "’"))
    description = TaskDescription(
        message=tasks.message.replace("'", "’"), task_id=task.slug
    )
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
    found_status.updated_at = datetime.now(timezone.utc)
    session.add(found_status)
    session.commit()


@app.delete("/delete-task", response_model=None)
async def delete_task(task: SlugTask, session: SessionDep):
    found_task = session.exec(select(TaskItem).where(TaskItem.slug == task.slug)).one()
    ic(found_task)
    session.delete(found_task)
    session.commit()


@app.delete("/delete-description", response_model=None)
async def delete_description(task: SlugTask, session: SessionDep):
    # TODO: probably should
    found_descr = session.exec(
        select(TaskDescription).where(TaskDescription.id == task.slug)
    ).one()
    ic(found_descr)
    session.delete(found_descr)
    session.commit()


@app.post("/create-description", response_model=None)
async def create_description(task: AddDescription, session: SessionDep):
    description = TaskDescription(
        message=task.content.replace("'", "’"), task_id=task.slug
    )
    session.add(description)
    session.commit()
    session.refresh(description)
    description.task.updated_at = datetime.now(timezone.utc)
    session.commit()


@app.put("/update-description", response_model=None)
async def update_description(description: AddDescription, session: SessionDep):
    # TODO: add slug to description potentially?
    found_des = session.get_one(TaskDescription, int(description.slug))
    found_des.message = description.content.replace("'", "’")
    found_des.updated_at = datetime.now(timezone.utc)
    session.add(found_des)
    session.commit()
    session.refresh(found_des)
    found_des.task.updated_at = datetime.now(timezone.utc)
    session.commit()


@app.patch("/change-title", response_model=None)
async def change_task_title(task: TitleTask, session: SessionDep):
    found_task = session.exec(select(TaskItem).where(TaskItem.slug == task.slug)).one()
    ic(found_task)
    found_task.title = task.title.replace("'", "’")
    session.add(found_task)
    session.commit()


@app.patch("/change-mailable", response_model=None)
async def change_mailing(mail_task: Mailibility, session: SessionDep):
    stmt = None
    match mail_task.kind:
        case "task":
            stmt = select(TaskItem).where(TaskItem.slug == mail_task.slug)
        case "description":
            stmt = select(TaskDescription).where(TaskDescription.id == mail_task.slug)
    found_item = session.exec(stmt).one()
    found_item.mailable = mail_task.flag
    session.add(found_item)
    ic(found_item)
    session.commit()
