from sqlmodel import SQLModel, Field
from datetime import date

class Usuario(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    cpf: str
    data_nascimento: date
    endereco: str
    senha: str

class Conta(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    usuario_id: int
    numero_conta: int
    agencia: str = "0001"
    saldo: float = 0.0
    numero_saques: int = 0
    limite_saques: int = 3
