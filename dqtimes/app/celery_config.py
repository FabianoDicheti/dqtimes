import os

class CeleryConfig:
    broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'America/Sao_Paulo'
    enable_utc = True
    
    task_track_started = True
    task_time_limit = 30 * 60
    task_soft_time_limit = 25 * 60
    
    result_expires = 3600
    result_persistent = True
    
    worker_prefetch_multiplier = 4
    worker_max_tasks_per_child = 1000
    worker_disable_rate_limits = False
    
    task_routes = {
        'app.tasks.forecast_task': {'queue': 'forecast_queue'},
        'app.tasks.process_dataframe_task': {'queue': 'forecast_queue'},
        'app.tasks.health_check': {'queue': 'default'},
    }
    
    task_default_queue = 'default'
    task_default_exchange = 'default'
    task_default_routing_key = 'default'
    
    broker_connection_retry_on_startup = True
    broker_connection_retry = True
    broker_connection_max_retries = 10
