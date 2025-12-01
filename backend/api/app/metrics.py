"""
Módulo de métricas customizadas para observabilidade do DQTimes.
Coleta métricas de RPS, latência, erros e métricas de negócio.
"""
from prometheus_client import Counter, Histogram, Gauge, Info
import time

# Métricas de requisições HTTP
http_requests_total = Counter(
    'dqtimes_http_requests_total',
    'Total de requisições HTTP recebidas',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'dqtimes_http_request_duration_seconds',
    'Duração das requisições HTTP em segundos',
    ['method', 'endpoint'],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0)
)

http_errors_total = Counter(
    'dqtimes_http_errors_total',
    'Total de erros HTTP',
    ['method', 'endpoint', 'error_type']
)

# Métricas de negócio - Projeções
projections_total = Counter(
    'dqtimes_projections_total',
    'Total de projeções geradas',
    ['endpoint', 'method_type']
)

projection_processing_duration_seconds = Histogram(
    'dqtimes_projection_processing_duration_seconds',
    'Tempo de processamento das projeções',
    ['endpoint'],
    buckets=(0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0)
)

dataset_size_processed = Histogram(
    'dqtimes_dataset_size_processed',
    'Tamanho dos datasets processados',
    ['endpoint'],
    buckets=(10, 50, 100, 500, 1000, 5000, 10000, 50000)
)

# Métricas de sistema
active_requests = Gauge(
    'dqtimes_active_requests',
    'Número de requisições ativas no momento'
)

# Informações da aplicação
app_info = Info(
    'dqtimes_app',
    'Informações da aplicação DQTimes'
)

# Inicializar informações da aplicação
app_info.info({
    'version': '1.0.0',
    'name': 'DQTimes API',
    'description': 'API de projeções temporais'
})


class MetricsMiddleware:
    """Middleware para coletar métricas de requisições HTTP."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Incrementar requisições ativas
        active_requests.inc()
        
        method = scope["method"]
        path = scope["path"]
        
        # Ignorar endpoint de métricas
        if path == "/metrics":
            active_requests.dec()
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        status_code = 500  # Default em caso de erro
        
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            # Registrar erro
            http_errors_total.labels(
                method=method,
                endpoint=path,
                error_type=type(e).__name__
            ).inc()
            raise
        finally:
            # Decrementar requisições ativas
            active_requests.dec()
            
            # Registrar duração
            duration = time.time() - start_time
            http_request_duration_seconds.labels(
                method=method,
                endpoint=path
            ).observe(duration)
            
            # Registrar total de requisições
            http_requests_total.labels(
                method=method,
                endpoint=path,
                status=status_code
            ).inc()


def track_projection(endpoint: str, method_type: str, dataset_size: int, processing_time: float):
    """
    Registra métricas de uma projeção realizada.
    
    Args:
        endpoint: Nome do endpoint que processou a projeção
        method_type: Tipo de método usado (HW, MA, etc)
        dataset_size: Tamanho do dataset processado
        processing_time: Tempo de processamento em segundos
    """
    projections_total.labels(
        endpoint=endpoint,
        method_type=method_type
    ).inc()
    
    projection_processing_duration_seconds.labels(
        endpoint=endpoint
    ).observe(processing_time)
    
    dataset_size_processed.labels(
        endpoint=endpoint
    ).observe(dataset_size)
