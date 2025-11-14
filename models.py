from __future__ import annotations
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

    contas: List[Conta] = Relationship(back_populates="usuario")


class Conta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agencia: str = Field(default="0001")
    numero_conta: int = Field(unique=True, index=True)
    saldo: float = Field(default=0.0)
    limite: float = Field(default=500.0)
    limite_saques: int = Field(default=3)
    numero_saques: int = Field(default=0)

    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="contas")
