from sqlmodel import Session, select
from models import Usuario, Conta
from datetime import date, datetime
from passlib.hash import bcrypt
from typing import Union, Optional

# ---------- Usuários ----------

def criar_usuario(
    session: Session,
    nome: str,
    cpf: str,
    data_nascimento: Union[str, date],
    endereco: str,
    senha: str
) -> Usuario:
    """Cria um novo usuário e retorna o objeto criado."""
    if isinstance(data_nascimento, str):
        data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()

    senha_hash = bcrypt.hash(senha)

    usuario = Usuario(
        nome=nome,
        cpf=cpf,
        data_nascimento=data_nascimento,
        endereco=endereco,
        senha=senha_hash
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def get_usuario(session: Session, cpf: str, senha: str) -> Optional[Usuario]:
    """Busca usuário pelo CPF e verifica a senha."""
    usuario = session.exec(
        select(Usuario).where(Usuario.cpf == cpf)
    ).first()

    if usuario and bcrypt.verify(senha, usuario.senha):
        return usuario
    return None

# ---------- Contas ----------

def criar_conta(session: Session, usuario: Usuario) -> Conta:
    """Cria uma nova conta para o usuário."""
    ultima_conta = session.exec(
        select(Conta).order_by(Conta.numero_conta.desc())
    ).first()
    numero_conta = (ultima_conta.numero_conta + 1) if ultima_conta else 1

    conta = Conta(usuario_id=usuario.id, numero_conta=numero_conta)
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return conta

def get_conta(session: Session, numero_conta: int) -> Optional[Conta]:
    """Busca conta pelo número."""
    return session.exec(
        select(Conta).where(Conta.numero_conta == numero_conta)
    ).first()

# ---------- Transações ----------

class TransacaoError(Exception):
    """Erro genérico para transações bancárias."""

def depositar(session: Session, conta: Conta, valor: float) -> None:
    if valor <= 0:
        raise TransacaoError("Valor do depósito deve ser maior que zero.")

    conta.saldo += valor
    session.add(conta)
    session.commit()
    session.refresh(conta)

def sacar(session: Session, conta: Conta, valor: float) -> None:
    if valor <= 0:
        raise TransacaoError("Valor do saque deve ser maior que zero.")
    if valor > conta.saldo:
        raise TransacaoError("Saldo insuficiente.")
    if conta.numero_saques >= conta.limite_saques:
        raise TransacaoError("Limite de saques atingido.")

    conta.saldo -= valor
    conta.numero_saques += 1
    session.add(conta)
    session.commit()
    session.refresh(conta)

def transferir(session: Session, origem: Conta, destino: Conta, valor: float) -> None:
    if valor <= 0:
        raise TransacaoError("Valor da transferência deve ser maior que zero.")
    if valor > origem.saldo:
        raise TransacaoError("Saldo insuficiente na conta de origem.")

    try:
        origem.saldo -= valor
        destino.saldo += valor
        session.add_all([origem, destino])
        session.commit()
        session.refresh(origem)
        session.refresh(destino)
    except Exception as e:
        session.rollback()
        raise TransacaoError(f"Erro na transferência: {str(e)}")