from sqlmodel import Session, select
from models import Usuario, Conta

def criar_usuario(session: Session, nome, cpf, data_nascimento, endereco, senha):
    usuario = Usuario(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco, senha=senha)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def get_usuario(session: Session, cpf, senha):
    return session.exec(select(Usuario).where(Usuario.cpf==cpf, Usuario.senha==senha)).first()

def criar_conta(session: Session, usuario: Usuario):
    ultima_conta = session.exec(select(Conta).order_by(Conta.numero_conta.desc())).first()
    numero_conta = (ultima_conta.numero_conta + 1) if ultima_conta else 1
    conta = Conta(usuario_id=usuario.id, numero_conta=numero_conta)
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return conta

def get_conta(session: Session, numero_conta: int):
    return session.exec(select(Conta).where(Conta.numero_conta==numero_conta)).first()

def depositar(session: Session, conta: Conta, valor: float):
    if valor <= 0:
        return False
    conta.saldo += valor
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return True

def sacar(session: Session, conta: Conta, valor: float):
    if valor <= 0 or valor > conta.saldo or conta.numero_saques >= conta.limite_saques:
        return False
    conta.saldo -= valor
    conta.numero_saques += 1
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return True

def transferir(session: Session, origem: Conta, destino: Conta, valor: float):
    if valor <= 0 or valor > origem.saldo:
        return False
    origem.saldo -= valor
    destino.saldo += valor
    session.add(origem)
    session.add(destino)
    session.commit()
    session.refresh(origem)
    session.refresh(destino)
    return True
