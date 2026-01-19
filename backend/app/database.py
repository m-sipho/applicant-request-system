from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./requests.db")

if "sqlite" in DATABASE_URL:
    connect_arg = {"check_same_thread": False}
else:
    connect_arg = {}

engine = create_engine(DATABASE_URL, connect_args=connect_arg, pool_size=20, max_overflow=10)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()