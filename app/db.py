# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

def get_sqlite_url(path: str = "sga_lite.db"):
    return f"sqlite:///{path}"

def get_engine(url: str | None = None):
    if url is None:
        url = os.getenv("DATABASE_URL", get_sqlite_url())
    # For SQLite: need check_same_thread for multithreading (FastAPI)
    if url.startswith("sqlite"):
        engine = create_engine(url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(url)
    return engine

def get_session_factory(engine=None):
    if engine is None:
        engine = get_engine()
    return sessionmaker(bind=engine, expire_on_commit=False)
