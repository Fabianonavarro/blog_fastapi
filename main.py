from fastapi import FastAPI
from database import init_db
from routers import contas

app = FastAPI()
app.include_router(contas.router)

@app.on_event("startup")
def on_startup():
    init_db()
