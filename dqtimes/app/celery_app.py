from celery import Celery
from app.celery_config import CeleryConfig

celery_app = Celery('dqtimes')
celery_app.config_from_object(CeleryConfig)
celery_app.autodiscover_tasks(['app'])
