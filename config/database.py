from sqlmodel import create_engine, SQLModel

sqlite_url = "sqlite:///tasks.db"

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
