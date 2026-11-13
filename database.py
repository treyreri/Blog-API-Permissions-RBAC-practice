from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine( DATABASE_URL, connect_args={"check_same_thread" : False}, )
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as session:
        yield session #yield позволяет сделать работу до эндпоинта (открыть) и после него (закрыть)