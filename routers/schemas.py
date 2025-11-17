from pydantic import BaseModel
from datetime import date

class UsuarioCreate(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    endereco: str
    senha: str

class ContaCreate(BaseModel):
    usuario_id: int
    numero_conta: int
