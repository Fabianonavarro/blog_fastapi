from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from crud import criar_usuario, get_usuario, criar_conta, get_conta, depositar, sacar, transferir
from schemas import UsuarioCreate, Login, Deposito, Saque, Transferencia, ContaOut, UsuarioOut

router = APIRouter()

# ---------- Usuários ----------
@router.post("/usuarios", response_model=UsuarioOut)
def criar_usuario_endpoint(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    return criar_usuario(
        nome=usuario.nome,
        cpf=usuario.cpf,
        data_nascimento=usuario.data_nascimento,
        endereco=usuario.endereco,
        senha=usuario.senha,
        session=session
    )

# ---------- Contas ----------
@router.post("/contas", response_model=ContaOut)
def criar_conta_endpoint(login: Login, session: Session = Depends(get_session)):
    usuario = get_usuario(login.cpf, login.senha, session=session)
    return criar_conta(usuario, session=session)

# ---------- Depósito ----------
@router.post("/deposito", response_model=ContaOut)
def depositar_endpoint(deposito: Deposito, session: Session = Depends(get_session)):
    conta = get_conta(deposito.numero_conta, session=session)
    depositar(conta, deposito.valor, session=session)
    return conta

# ---------- Saque ----------
@router.post("/saque", response_model=ContaOut)
def sacar_endpoint(saque_data: Saque, session: Session = Depends(get_session)):
    conta = get_conta(saque_data.numero_conta, session=session)
    sacar(conta, saque_data.valor, session=session)
    return conta

# ---------- Transferência ----------
@router.post("/transferencia", response_model=dict)
def transferir_endpoint(transf: Transferencia, session: Session = Depends(get_session)):
    conta_origem = get_conta(transf.origem, session=session)
    conta_destino = get_conta(transf.destino, session=session)
    transferir(conta_origem, conta_destino, transf.valor, session=session)
    return {
        "origem": conta_origem.numero_conta,
        "saldo_origem": conta_origem.saldo,
        "destino": conta_destino.numero_conta,
        "saldo_destino": conta_destino.saldo
    }
