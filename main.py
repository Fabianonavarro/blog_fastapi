from fastapi import FastAPI
from routers import contas  # import absoluto
from database import init_db

app = FastAPI(title="Blog FastAPI")

# Inicializa o banco
init_db()

# Inclui os routers
app.include_router(contas.router)

# Rota raiz
@app.get("/")
def raiz():
    return {"message": "API Online! Acesse /usuarios, /contas, /deposito, /saque, /transferencia"}
