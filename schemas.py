from pydantic import BaseModel, ConfigDict, Field
from datetime import date


# ---------- Usuários ----------

class UsuarioCreate(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    endereco: str
    senha: str


class UsuarioOut(BaseModel):
    id: int
    nome: str
    cpf: str
    data_nascimento: date
    endereco: str

    model_config = ConfigDict(from_attributes=True)


class Login(BaseModel):
    cpf: str
    senha: str


# ---------- Contas ----------

class ContaOut(BaseModel):
    numero_conta: int
    saldo: float

    model_config = ConfigDict(from_attributes=True)


# ---------- Transações ----------

class Deposito(BaseModel):
    numero_conta: int
    valor: float = Field(gt=0, description="Valor do depósito deve ser maior que zero")


class Saque(BaseModel):
    numero_conta: int
    valor: float = Field(gt=0, description="Valor do saque deve ser maior que zero")


class Transferencia(BaseModel):
    origem: int
    destino: int
    valor: float = Field(gt=0, description="Valor da transferência deve ser maior que zero")