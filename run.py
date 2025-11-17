# run.py
import uvicorn
from fastapi import FastAPI
from database import init_db
from routers import usuarios  # seu router de usuários/contas

# ---------- Inicializa banco ----------
init_db()

# ---------- Cria app ----------
app = FastAPI(title="Banco FastAPI", version="1.0")

# ---------- Inclui routers ----------
app.include_router(usuarios.router, prefix="/api", tags=["Banco"])

# ---------- Roda servidor ----------
if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True)
