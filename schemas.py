from pydantic import BaseModel
from datetime import date

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

    class Config:
        orm_mode = True

class Login(BaseModel):
    cpf: str
    senha: str

class ContaOut(BaseModel):
    numero_conta: int
    saldo: float

    class Config:
        orm_mode = True

class Deposito(BaseModel):
    numero_conta: int
    valor: float

class Saque(BaseModel):
    numero_conta: int
    valor: float

class Transferencia(BaseModel):
    origem: int
    destino: int
    valor: float
