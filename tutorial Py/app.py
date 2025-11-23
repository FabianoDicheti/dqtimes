from fastapi import FastAPI, Query
from services.meu_servico import Minha_Classe
from models import (
    Exemplo1Response, 
    Exemplo2Response
)

app = FastAPI(
    title="Microserviço xablau",
    description="API da quinta-feira",
    version="2.9.9"
)

servico = Minha_Classe()


@app.get("/exemplo1", response_model=Exemplo1Response)
def exemplo1() -> Exemplo1Response:
    """ neste endipoint adhakjsdhfkljasdhfkljasdhfkçasdjhf
    recebe oihjcaksldjflkçasdjf
    retorna aiudhfalkjdhfliajkh
    """

    resultado = servico.exemplo_variaveis_tipos()
    return Exemplo1Response(**resultado)

@app.get("/exemplo2", response_model=Exemplo2Response)
def exemplo2(
    iteracoes: int = Query(
        default=10000, 
        ge=1, 
        le=1000000, 
        description="Numero de itens do for"
    )
) -> Exemplo2Response:

    resultado = servico.exemplo_performance_for(iteracoes)
    return Exemplo2Response(**resultado)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

