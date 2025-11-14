from sqlmodel import SQLModel, create_engine, Session

# Caminho relativo (Render cria em /opt/render/project/src/)
sqlite_url = "sqlite:///banco.db"

engine = create_engine(sqlite_url, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    from .models import Usuario, Conta
    SQLModel.metadata.create_all(engine)
