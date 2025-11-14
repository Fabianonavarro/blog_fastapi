from sqlmodel import Session, select
from models import Usuario, Conta
import random

# ---------- Usuário ----------
def criar_usuario(session: Session, nome, cpf, data_nascimento, endereco, senha):
    usuario = Usuario(
        nome=nome,
        cpf=cpf,
        data_nascimento=data_nascimento,
        endereco=endereco,
        senha=senha
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def get_usuario(session: Session, cpf, senha):
    statement = select(Usuario).where(Usuario.cpf == cpf, Usuario.senha == senha)
    result = session.exec(statement).first()
    return result

# ---------- Conta ----------
def criar_conta(session: Session, usuario: Usuario):
    numero_conta = random.randint(10000, 99999)
    conta = Conta(numero_conta=numero_conta, usuario_id=usuario.id)
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return conta

def get_conta(session: Session, numero_conta: int):
    statement = select(Conta).where(Conta.numero_conta == numero_conta)
    return session.exec(statement).first()

def depositar(session: Session, conta: Conta, valor: float):
    if valor <= 0:
        return False
    conta.saldo += valor
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return True

def sacar(session: Session, conta: Conta, valor: float):
    if valor <= 0 or conta.numero_saques >= conta.limite_saques or conta.saldo + conta.limite < valor:
        return False
    conta.saldo -= valor
    conta.numero_saques += 1
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return True

def transferir(session: Session, origem: Conta, destino: Conta, valor: float):
    if not sacar(session, origem, valor):
        return False
    depositar(session, destino, valor)
    return True
