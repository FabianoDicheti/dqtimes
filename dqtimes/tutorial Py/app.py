from fastapi import FastAPI, Query, HTTPException
from services.meu_servico import Minha_Classe
from services.time_series import Minha_Classe as TimeSeries

from models import (
    Exemplo1Response, 
    Exemplo2Response,
    Exemplo3Response
)

app = FastAPI(
    title="Microserviço xablau",
    description="API da quinta-feira",
    version="2.9.9"
)   


servico = Minha_Classe()
servico_ts = TimeSeries()


@app.get("/exemplo1", response_model=Exemplo1Response)
def exemplo1() -> Exemplo1Response:
    """ neste endipoint adhakjsdhfkljasdhfkljasdhfkçasdjhf
    recebe oihjcaksldjflkçasdjf
    retorna aiudhfalkjdhfliajkh
    """

    resultado = servico.exemplo_variaveis_tipos()
    return Exemplo1Response(**resultado)

@app.get("/exemplo3", response_model=Exemplo3Response)
def exemplo3(
    lista: str = Query(..., description="Lista de valores float separados por vírgula"),
    qnt: str = Query(..., description="Quantidade de previsões (string)")
) -> Exemplo3Response:
    """Endpoint exemplo 3 - Médias móveis"""
    
    try:
        lista_floats = [float(x.strip()) for x in lista.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="Lista inválida. Use apenas números separados por vírgula.")

    try:
        qnt_int = int(qnt)
        if qnt_int <= 0:
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=400, detail="qnt deve ser um inteiro maior que 0.")

    # USA O SERVIÇO DE TIME SERIES
    resultado = servico_ts.exemplo3_medias_moveis(lista_floats, qnt_int)
    return resultado



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

