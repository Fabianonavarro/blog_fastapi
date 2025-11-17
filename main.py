from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from routers import contas

app = FastAPI(title="Blog FastAPI - Banco")

# Cria as tabelas automaticamente
SQLModel.metadata.create_all(engine)

# Rotas
app.include_router(contas.router)
