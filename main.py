from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import init_db
from routers import contas
from exceptions import AccountNotFoundError, BusinessError

app = FastAPI(title="Transactions API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(contas.router, tags=["account"])

# Exceções
@app.exception_handler(AccountNotFoundError)
async def handle_account_not_found(request: Request, exc: AccountNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Account not found."})

@app.exception_handler(BusinessError)
async def handle_business_error(request: Request, exc: BusinessError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

# Cria tabelas
init_db()
