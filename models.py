from sqlmodel import SQLModel, Field
from datetime import date

# ---------- Usuário ----------
class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    cpf: str = Field(max_length=11, unique=True, index=True)
    data_nascimento: date
    endereco: str = Field(max_length=200)
    senha: str = Field(max_length=100)

# ---------- Conta ----------
class Conta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    numero_conta: int = Field(index=True)
    agencia: str = Field(default="0001", max_length=10)
    saldo: float = Field(default=0.0)
    numero_saques: int = Field(default=0)
    limite_saques: int = Field(default=3)
