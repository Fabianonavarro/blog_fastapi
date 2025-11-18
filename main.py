from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from routers import usuarios

app = FastAPI(
    title="API Bancária FastAPI",
    description="API simples de usuários, contas e transações bancárias",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(usuarios.router, prefix="/api", tags=["Usuários e Contas"])

@app.get("/")
def root():
    return {"mensagem": "API Bancária funcionando!"}
