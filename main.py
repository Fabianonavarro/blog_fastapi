'''from fastapi import FastAPI
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
'''

from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from database import engine, get_session
from models import Usuario, Conta

app = FastAPI(title="API de Banco")

# Inicializa o banco ao subir a aplicação
@app.on_event("startup")
def on_startup():
    from models import Usuario, Conta
    Usuario.metadata.create_all(engine)
    Conta.metadata.create_all(engine)

# Rota raiz
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

# Cadastrar usuário
@app.post("/usuarios/")
def criar_usuario(usuario: Usuario):
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

# Cadastrar conta
@app.post("/contas/")
def criar_conta(conta: Conta):
    with Session(engine) as session:
        # Verifica se o usuário existe
        usuario = session.get(Usuario, conta.usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        session.add(conta)
        session.commit()
        session.refresh(conta)
        return conta

# Consultar saldo de uma conta
@app.get("/contas/{conta_id}/saldo")
def ver_saldo(conta_id: int):
    with Session(engine) as session:
        conta = session.get(Conta, conta_id)
        if not conta:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
        return {"saldo": conta.saldo, "numero_conta": conta.numero_conta}
