from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import engine, get_session
from models import Usuario, Conta
from schemas import UsuarioCreate, ContaCreate

app = FastAPI(title="API de Banco")

# Criar tabelas no Postgres na inicialização
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Rota raiz
@app.get("/")
def root(session: Session = Depends(get_session)):
    total_usuarios = session.exec(select(Usuario)).all()
    total_contas = session.exec(select(Conta)).all()
    return {
        "total_usuarios": len(total_usuarios),
        "total_contas": len(total_contas),
        "mensagem": "API está rodando!"
    }

# Criar usuário
@app.post("/usuarios/")
def criar_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    novo = Usuario(**usuario.dict())
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return novo

# Criar conta
@app.post("/contas/")
def criar_conta(conta: ContaCreate, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, conta.usuario_id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    nova_conta = Conta(**conta.dict())
    session.add(nova_conta)
    session.commit()
    session.refresh(nova_conta)
    return nova_conta

# Ver saldo
@app.get("/contas/{conta_id}/saldo")
def ver_saldo(conta_id: int, session: Session = Depends(get_session)):
    conta = session.get(Conta, conta_id)

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    return {
        "numero_conta": conta.numero_conta,
        "saldo": conta.saldo
    }
