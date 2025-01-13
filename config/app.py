from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from inertia import (
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,
    inertia_request_validation_exception_handler,
)
from config.database import create_db_and_tables
from config.views import static_dir

app_key = "3eef539b6e0bb1ec1539bd91f4b101f9"


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events
    """
    create_db_and_tables()
    yield  # FastAPI runs here


app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=app_key)

app.add_exception_handler(
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    RequestValidationError,
    inertia_request_validation_exception_handler,  # type: ignore[arg-type]
)

app.mount("/static", StaticFiles(directory=static_dir), name=f"static")
