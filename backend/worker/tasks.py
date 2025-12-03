import os
import sys
# Adiciona a pasta libs ao caminho do Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

from celery_app import app

# Importa direto das libs Rust
from hot_winters import previsao_hot_winters
from medias_autoregressivas import previsao_media_autoregressiva
from medias_exponenciais import previsao_media_exponencial
from interpolador1d import interpolador1d

@app.task
def prever(dados: list, horizonte: int, metodo: str = "hot_winters"):
    if metodo == "hot_winters":
        return previsao_hot_winters(dados, horizonte)
    elif metodo == "media_autoregressiva":
        return previsao_media_autoregressiva(dados, horizonte)
    else:
        return {"erro": "método não suportado"}