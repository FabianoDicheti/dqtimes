from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import time

router = APIRouter(prefix="/tasks", tags=["tasks"])

class TaskRequest(BaseModel):
    lista_historico: list
    quantidade_projecoes: int

class TaskResponse(BaseModel):
    task_id: str
    status: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None

try:
    from app.celery_app import celery_app
    from app.tasks import forecast_task, dummy_task
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False

@router.post("/forecast", response_model=TaskResponse)
async def create_forecast_task(request: TaskRequest):
    if not CELERY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Celery not available")
    
    task = forecast_task.delay(request.lista_historico, request.quantidade_projecoes)
    
    return TaskResponse(
        task_id=task.id,
        status="pending"
    )

@router.post("/dummy", response_model=TaskResponse)
async def create_dummy_task(wait_seconds: int = 5):
    if not CELERY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Celery not available")
    
    task = dummy_task.delay(wait_seconds)
    
    return TaskResponse(
        task_id=task.id,
        status="pending"
    )

@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    if not CELERY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Celery not available")
    
    task = celery_app.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = TaskStatusResponse(
            task_id=task_id,
            status="pending",
            result=None
        )
    elif task.state == 'STARTED':
        response = TaskStatusResponse(
            task_id=task_id,
            status="running",
            result=None
        )
    elif task.state == 'SUCCESS':
        response = TaskStatusResponse(
            task_id=task_id,
            status="completed",
            result=task.result
        )
    elif task.state == 'FAILURE':
        response = TaskStatusResponse(
            task_id=task_id,
            status="failed",
            error=str(task.info)
        )
    else:
        response = TaskStatusResponse(
            task_id=task_id,
            status=task.state.lower(),
            result=None
        )
    
    return response
