from fastapi import FastAPI, Query
from services.example_service import Minha_Classe
from models import (
    Exemplo1Response, 
    Exemplo2Response
)

app = FastAPI(
    title="Microserviço Time-series",
    description="API dqtimes",
    version="2.9.9"
)

servico = Minha_Classe()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Time-series Microservice!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

