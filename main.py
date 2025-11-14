from fastapi import FastAPI
from .routers import contas
import os

app = FastAPI(title="API Bancario")

# Rota principal
@app.get("/")
def root():
    return {"message": "API Bancario rodando!"}

# Incluir o router das contas
app.include_router(contas.router, prefix="/contas")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
