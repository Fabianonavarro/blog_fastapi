from fastapi import FastAPI
from sqlmodel import Session, select, SQLModel
from database import engine
from models import Usuario, Conta

app = FastAPI()

# Inicializa o banco ao subir a aplicação
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Rota raiz funcional: mostra número de usuários e contas
@app.get("/")
def root():
    with Session(engine) as session:
        total_usuarios = session.exec(select(Usuario)).all()
        total_contas = session.exec(select(Conta)).all()
        return {
            "total_usuarios": len(total_usuarios),
            "total_contas": len(total_contas),
            "mensagem": "API está rodando!"
        }
