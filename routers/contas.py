from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from crud import criar_usuario, get_usuario, criar_conta, get_conta, depositar, sacar, transferir
from schemas import UsuarioCreate, Login, Deposito, Saque, Transferencia

router = APIRouter()


# ---------- Usuários ----------
@router.post("/usuarios")
def criar_usuario_endpoint(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    usuario_criado = criar_usuario(
        session,
        nome=usuario.nome,
        cpf=usuario.cpf,
        data_nascimento=usuario.data_nascimento,
        endereco=usuario.endereco,
        senha=usuario.senha
    )
    return {"id": usuario_criado.id, "nome": usuario_criado.nome}


# ---------- Contas ----------
@router.post("/contas")
def criar_conta_endpoint(login: Login, session: Session = Depends(get_session)):
    usuario = get_usuario(session, login.cpf, login.senha)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou senha incorreta")
    conta = criar_conta(session, usuario)
    return {"numero_conta": conta.numero_conta, "agencia": conta.agencia, "saldo": conta.saldo}


# ---------- Depósito ----------
@router.post("/deposito")
def depositar_endpoint(deposito: Deposito, session: Session = Depends(get_session)):
    conta = get_conta(session, deposito.numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    if not depositar(session, conta, deposito.valor):
        raise HTTPException(status_code=400, detail="Depósito inválido")
    return {"saldo": conta.saldo}


# ---------- Saque ----------
@router.post("/saque")
def sacar_endpoint(saque_data: Saque, session: Session = Depends(get_session)):
    conta = get_conta(session, saque_data.numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    if not sacar(session, conta, saque_data.valor):
        raise HTTPException(status_code=400, detail="Saque inválido")
    return {"saldo": conta.saldo}


# ---------- Transferência ----------
@router.post("/transferencia")
def transferir_endpoint(transf: Transferencia, session: Session = Depends(get_session)):
    conta_origem = get_conta(session, transf.origem)
    conta_destino = get_conta(session, transf.destino)
    if not conta_origem or not conta_destino:
        raise HTTPException(status_code=404, detail="Conta(s) não encontrada(s)")
    if not transferir(session, conta_origem, conta_destino, transf.valor):
        raise HTTPExceptio
