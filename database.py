from sqlmodel import SQLModel, create_engine, Session

SQLITE_URL = "sqlite:///banco.db"

engine = create_engine(SQLITE_URL, echo=False)

def init_db():
    from models import Usuario, Conta
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
