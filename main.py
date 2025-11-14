from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from database import engine, database
from models import Usuario, Conta

app = FastAPI()

# Incluindo routers se houver
# app.include_router(contas.router)

# Inicializa o banco ao subir a aplicação
@app.on_event("startup")
async def startup():
    await database.connect()
    from models import Usuario, Conta
    Usuario.metadata.create_all(engine)
    Conta.metadata.create_all(engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Rota raiz funcional: mostra número de usuários e contas
@app.get("/")
async def root():
    with Session(engine) as session:
        total_usuarios = session.exec(select(Usuario)).all()
        total_contas = session.exec(select(Conta)).all()
        return {
            "total_usuarios": len(total_usuarios),
            "total_contas": len(total_contas),
            "mensagem": "API está rodando!"
        }
