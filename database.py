import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não foi configurada no ambiente!")

engine = create_engine(
    DATABASE_URL,
    echo=False,  # evita travar no Render
    pool_pre_ping=True,  # evita conexões quebradas
)

def get_session():
    with Session(engine) as session:
        yield session
