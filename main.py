from fastapi import FastAPI
from database import init_db
from routers.contas import router as contas_router

app = FastAPI(title="Blog FastAPI - Banco")

# Inicializa o banco de dados e tabelas
init_db()

# Inclui rotas do módulo contas com prefixo /api
app.include_router(contas_router, prefix="/api")

# Rota raiz para teste de funcionamento
@app.get("/")
def root():
    return {"message": "API Blog FastAPI funcionando!"}
