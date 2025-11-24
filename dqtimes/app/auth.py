from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(dados: LoginRequest):
    usuario_valido = "admin"
    senha_valida = "123"

    if dados.username == usuario_valido and dados.password == senha_valida:
        return {
            "mensagem": "Login realizado com sucesso!",
            "token": "token", 
            "usuario": dados.username
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos"
        )