from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

sqlite_url = "sqlite:///storage/db/tasks.db"

engine = create_engine(
    sqlite_url,
    connect_args={
        "check_same_thread": False,
    },
)


def create_db_and_tables():
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
        conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
