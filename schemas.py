from pydantic import BaseModel, Field
from datetime import date

# ---------- Usuários ----------
class UsuarioCreate(BaseModel):
    nome: str = Field(..., example="João Silva")
    cpf: str = Field(..., example="12345678900")
    data_nascimento: date = Field(..., example="1990-01-01")
    endereco: str = Field(..., example="Rua Exemplo, 123")
    senha: str = Field(..., example="senhaSegura123")


class UsuarioOut(BaseModel):
    id: int
    nome: str


# ---------- Login ----------
class Login(BaseModel):
    cpf: str = Field(..., example="12345678900")
    senha: str = Field(..., example="senhaSegura123")


# ---------- Transações ----------
class Deposito(BaseModel):
    numero_conta: int = Field(..., example=1)
    valor: float = Field(..., example=100.0)


class Saque(BaseModel):
    numero_conta: int = Field(..., example=1)
    valor: float = Field(..., example=50.0)


class Transferencia(BaseModel):
    origem: int = Field(..., example=1)
    destino: int = Field(..., example=2)
    valor: float = Field(..., example=75.0)


# ---------- Contas ----------
class ContaOut(BaseModel):
    numero_conta: int
    agencia: str
    saldo: float
