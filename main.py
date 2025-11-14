from fastapi import FastAPI
from routers import contas  # import absoluto
import os

app = FastAPI(title="API Bancario")

# Rota principal
@app.get("/")
def root():
    return {"message": "API Bancario rodando!"}

# Incluir o router das contas
app.include_router(contas.router, prefix="/contas")
