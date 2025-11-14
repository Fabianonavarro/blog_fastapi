from sqlmodel import Session, select
from models import Usuario, Conta

# ---------- Usuários ----------
def criar_usuario(session: Session, nome, cpf, data_nascimento, endereco, senha):
    usuario = Usuario(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco, senha=senha)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def get_usuario(session: Session, cpf, senha):
    stmt = select(Usuario).where(Usuario.cpf == cpf, Usuario.senha == senha)
    return session.exec(stmt).first()


# ---------- Contas ----------
def criar_conta(session: Session, usuario: Usuario):
    # Cria conta com número único simples
    numero = session.exec(select(Conta.numero_conta)).all()
    numero_conta = max(numero) + 1 if numero else 1
    conta = Conta(usuario_id=usuario.id, numero_conta=numero_conta)
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return conta

def get_conta(session: Session, numero_conta: int):
    stmt = select(Conta).where(Conta.numero_conta == numero_conta)
    return session.exec(stmt).first()

def depositar(session: Session, conta: Conta, valor: float):
    if valor <= 0:
        return False
    conta.saldo += valor
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return True

def sacar(session: Session, conta: Conta, valor: float):
    if valor <= 0 or conta.saldo + conta.limite < valor or conta.numero_saques >= conta.limite_saques:
        return False
    conta.saldo -= valor
    conta.numero_saques += 1
    session.add(conta)
    session.commit()
    session.refresh(conta)
    return True

def transferir(session: Session, origem: Conta, destino: Conta, valor: float):
    if valor <= 0 or origem.saldo + origem.limite < valor:
        return False
    origem.saldo -= valor
    destino.saldo += valor
    session.add(origem)
    session.add(destino)
    session.commit()
    session.refresh(origem)
    session.refresh(destino)
    return True
