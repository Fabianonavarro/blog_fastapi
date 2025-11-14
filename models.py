from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cpf: str = Field(unique=True, index=True)
    data_nascimento: date
    endereco: str
    senha: str

    # Relacionamento com Contas (sem default_factory)
    contas: List["Conta"] = Relationship(
        back_populates="usuario",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Conta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agencia: str = Field(default="0001")
    numero_conta: int = Field(index=True, unique=True)
    saldo: float = Field(default=0.0)
    limite: float = Field(default=500.0)
    limite_saques: int = Field(default=3)
    numero_saques: int = Field(default=0)

    # Relacionamento com Usuario
    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="contas")
