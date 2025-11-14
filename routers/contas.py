from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..crud import criar_usuario, get_usuario, criar_conta, get_conta, depositar, sacar, transferir
from ..schemas import UsuarioCreate, Login, Deposito, Saque, Transferencia

router = APIRouter()

# ---------- Usuários ----------
@router.post("/usuarios")
def criar_usuario_endpoint(dados: UsuarioCreate, session: Session = Depends(get_session)):
    usuario = criar_usuario(
        session,
        dados.nome,
        dados.cpf,
        dados.data_nascimento,
        dados.endereco,
        dados.senha
    )
    return {"id": usuario.id, "nome": usuario.nome}


# ---------- Contas ----------
@router.post("/contas")
def criar_conta_endpoint(login: Login, session: Session = Depends(get_session)):
    usuario = get_usuario(session, login.cpf, login.senha)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou senha incorreta")

    conta = criar_conta(session, usuario)
    return {
        "numero_conta": conta.numero_conta,
        "agencia": conta.agencia,
        "saldo": conta.saldo
    }


# ---------- Depósito ----------
@router.post("/deposito")
def depositar_endpoint(dados: Deposito, session: Session = Depends(get_session)):
    conta = get_conta(session, dados.numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if not depositar(session, conta, dados.valor):
        raise HTTPException(status_code=400, detail="Depósito inválido")

    return {"saldo": conta.saldo}


# ---------- Saque ----------
@router.post("/saque")
def sacar_endpoint(dados: Saque, session: Session = Depends(get_session)):
    conta = get_conta(session, dados.numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if not sacar(session, conta, dados.valor):
        raise HTTPException(status_code=400, detail="Saque inválido")

    return {"saldo": conta.saldo}


# ---------- Transferência ----------
@router.post("/transferencia")
def transferir_endpoint(dados: Transferencia, session: Session = Depends(get_session)):
    conta_origem = get_conta(session, dados.origem)
    conta_destino = get_conta(session, dados.destino)

    if not conta_origem or not conta_destino:
        raise HTTPException(status_code=404, detail="Conta(s) não encontrada(s)")

    if not transferir(session, conta_origem, conta_destino, dados.valor):
        raise HTTPException(status_code=400, detail="Transferência inválida")

    return {
        "saldo_origem": conta_origem.saldo,
        "saldo_destino": conta_destino.saldo
    }
