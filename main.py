from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import database  # ajuste para seu módulo
from routers import contas, auth, transaction  # ajuste caso precise
from exceptions import AccountNotFoundError, BusinessError  # crie esse arquivo/exceções se não existirem


# Lifespan para conectar e desconectar o DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


tags_metadata = [
    {"name": "auth", "description": "Operations for authentication."},
    {"name": "account", "description": "Operations to maintain accounts."},
    {"name": "transaction", "description": "Operations to maintain transactions."},
]


app = FastAPI(
    title="Transactions API",
    version="1.0.0",
    summary="Microservice to maintain withdrawal and deposit operations from current accounts.",
    description="""
Transactions API is the microservice for recording current account transactions. 💸💰

## Account

* **Create accounts**.
* **List accounts**.
* **List account transactions by ID**.

## Transaction

* **Create transactions**.
""",
    openapi_tags=tags_metadata,
    redoc_url=None,
    lifespan=lifespan,
)


# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(auth.router, tags=["auth"])
app.include_router(contas.router, tags=["account"])  # seu router de contas
app.include_router(transaction.router, tags=["transaction"])


# Handlers de exceção
@app.exception_handler(AccountNotFoundError)
async def account_not_found_error_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Account not found."})


@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})
