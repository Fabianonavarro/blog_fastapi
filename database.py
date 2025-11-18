import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env local (útil para desenvolvimento)
load_dotenv()

# Obtém a URL do banco de dados do ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não foi configurada no ambiente!")

# Cria o engine com suporte a reconexão automática
engine = create_engine(
    DATABASE_URL,
    echo=True,              # Mostra as queries no console (útil para debug)
    pool_pre_ping=True      # Verifica conexão antes de usar (evita timeouts)
)

# Gerador de sessões para uso com Depends no FastAPI
def get_session():
    with Session(engine) as session:
        yield session