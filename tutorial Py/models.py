from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union

class ExemploTipo(BaseModel):
    valor: Union[int, float, str, bool, List[int]]
    tipo: str
    operacao: str = None
    tamanho: int = None

class Exemplo1Response(BaseModel):
    conceito: str
    explicacao: str
    exemplos: Dict[str, ExemploTipo]

class ParametrosPerformance(BaseModel):
    iteracoes: int
    operacao: str

class ResultadoTeste(BaseModel):
    tempo_segundos: float
    codigo_exemplo: str

class ResultadosPerformance(BaseModel):
    for_normal: ResultadoTeste
    list_comprehension: ResultadoTeste

class AnalisePerformance(BaseModel):
    mais_rapido: str
    diferenca_percentual: float
    conclusao: str

class VerificacaoResultado(BaseModel):
    resultados_iguais: bool
    tamanho_resultado: int

class Exemplo2Response(BaseModel):
    conceito: str
    explicacao: str
    parametros: ParametrosPerformance
    resultados: ResultadosPerformance
    analise: AnalisePerformance
    verificacao: VerificacaoResultado

class EndpointInfo(BaseModel):
    mensagem: str
    endpoints_disponiveis: List[str]

class PerformanceRequest(BaseModel):
    iteracoes: int = Field(default=10000, ge=1, le=1000000, description="Número de iterações para o teste de performance")

