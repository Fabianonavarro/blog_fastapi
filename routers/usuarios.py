from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from crud import (
    criar_usuario, get_usuario, criar_conta, get_conta,
    depositar, sacar, transferir, TransacaoError
)
from schemas import (
    UsuarioCreate, Login, Deposito, Saque,
    Transferencia, ContaOut, UsuarioOut
)

router = APIRouter()


# ---------- Usuários ----------

@router.post("/usuarios", response_model=UsuarioOut, status_code=201)
def criar_usuario_endpoint(
    usuario: UsuarioCreate,
    session: Session = Depends(get_session)
):
    return criar_usuario(
        session,
        usuario.nome,
        usuario.cpf,
        usuario.data_nascimento,
        usuario.endereco,
        usuario.senha
    )


# ---------- Contas ----------

@router.post("/contas", response_model=ContaOut, status_code=201)
def criar_conta_endpoint(
    login: Login,
    session: Session = Depends(get_session)
):
    usuario = get_usuario(session, login.cpf, login.senha)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou senha incorreta")
    return criar_conta(session, usuario)


# ---------- Depósito ----------

@router.post("/deposito", response_model=ContaOut)
def depositar_endpoint(
    deposito: Deposito,
    session: Session = Depends(get_session)
):
    conta = get_conta(session, deposito.numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    try:
        depositar(session, conta, deposito.valor)
    except TransacaoError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return conta


# ---------- Saque ----------

@router.post("/saque", response_model=ContaOut)
def sacar_endpoint(
    saque_data: Saque,
    session: Session = Depends(get_session)
):
    conta = get_conta(session, saque_data.numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    try:
        sacar(session, conta, saque_data.valor)
    except TransacaoError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return conta


# ---------- Transferência ----------

@router.post("/transferencia", response_model=dict)
def transferir_endpoint(
    transf: Transferencia,
    session: Session = Depends(get_session)
):
    conta_origem = get_conta(session, transf.origem)
    conta_destino = get_conta(session, transf.destino)

    if not conta_origem or not conta_destino:
        raise HTTPException(status_code=404, detail="Conta(s) não encontrada(s)")

    try:
        transferir(session, conta_origem, conta_destino, transf.valor)
    except TransacaoError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "origem": conta_origem.numero_conta,
        "saldo_origem": conta_origem.saldo,
        "destino": conta_destino.numero_conta,
        "saldo_destino": conta_destino.saldo
    }