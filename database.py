from databases import Database
from sqlmodel import SQLModel, create_engine

# Caminho do SQLite
SQLITE_URL = "sqlite:///banco.db"

# Objeto database para async
database = Database(SQLITE_URL)

# Engine para criar tabelas (síncrono)
engine = create_engine(SQLITE_URL, echo=False)

def init_db():
    from models import Usuario, Conta  # ajuste para seu módulo
    SQLModel.metadata.create_all(engine)
