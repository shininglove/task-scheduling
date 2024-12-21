from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from inertia import (
    InertiaResponse,
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,
    inertia_request_validation_exception_handler,
)
from config import InertiaDependency, views_dir

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="message")

app.add_exception_handler(
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    RequestValidationError,
    inertia_request_validation_exception_handler,  # type: ignore[arg-type]
)

app.mount("/static", StaticFiles(directory=views_dir), name=f"{views_dir}")


@app.get("/", response_model=None)
async def index(inertia: InertiaDependency) -> InertiaResponse:
    return await inertia.render("Index", {"name": "Connor"})
