from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from crud import criar_usuario, get_usuario, criar_conta, get_conta, depositar, sacar, transferir

router = APIRouter()

# ---------- Usuários ----------
@router.post("/usuarios")
def criar_usuario_endpoint(nome: str, cpf: str, data_nascimento: str, endereco: str, senha: str,
                           session: Session = Depends(get_session)):
    usuario = criar_usuario(session, nome, cpf, data_nascimento, endereco, senha)
    return {"id": usuario.id, "nome": usuario.nome}

# ---------- Contas ----------
@router.post("/contas")
def criar_conta_endpoint(cpf: str, senha: str, session: Session = Depends(get_session)):
    usuario = get_usuario(session, cpf, senha)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou senha incorreta")
    conta = criar_conta(session, usuario)
    return {"numero_conta": conta.numero_conta, "agencia": conta.agencia, "saldo": conta.saldo}

@router.post("/deposito")
def depositar_endpoint(numero_conta: int, valor: float, session: Session = Depends(get_session)):
    conta = get_conta(session, numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    if not depositar(session, conta, valor):
        raise HTTPException(status_code=400, detail="Depósito inválido")
    return {"saldo": conta.saldo}

@router.post("/saque")
def sacar_endpoint(numero_conta: int, valor: float, session: Session = Depends(get_session)):
    conta = get_conta(session, numero_conta)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    if not sacar(session, conta, valor):
        raise HTTPException(status_code=400, detail="Saque inválido")
    return {"saldo": conta.saldo}

@router.post("/transferencia")
def transferir_endpoint(origem: int, destino: int, valor: float, session: Session = Depends(get_session)):
    conta_origem = get_conta(session, origem)
    conta_destino = get_conta(session, destino)
    if not conta_origem or not conta_destino:
        raise HTTPException(status_code=404, detail="Conta(s) não encontrada(s)")
    if not transferir(session, conta_origem, conta_destino, valor):
        raise HTTPException(status_code=400, detail="Transferência inválida")
    return {"saldo_origem": conta_origem.saldo, "saldo_destino": conta_destino.saldo}
