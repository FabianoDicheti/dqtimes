from typing import Optional, List, Any
from fastapi import FastAPI, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
import math
import os

from .database import engine, Base, get_db
from .models import TaskHistory, HistoryResponse, HistoryItemExpanded, Link

app = FastAPI()

Base.metadata.create_all(bind=engine)

DEFAULT_PAGE = int(os.getenv("DEFAULT_PAGE", 1))
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", 25))
DEFAULT_DETAILS = os.getenv("DEFAULT_DETAILS", "True").lower() in ("true", "1", "yes")

def format_number_in_dict(data: Any, precision: int = 4) -> Any:
    if isinstance(data, dict):
        return {k: format_number_in_dict(v, precision) for k, v in data.items()}
    elif isinstance(data, list):
        return [format_number_in_dict(item, precision) for item in data]
    elif isinstance(data, float):
        return round(data, precision)
    return data

def build_pagination_links(request: Request, total_pages: int, page: int, limit: int) -> List[Link]:
    base_url = str(request.url).split('?')[0]
    
    def generate_url(p: int) -> str:
        params = dict(request.query_params)
        params['page'] = str(p)
        params['limit'] = str(limit)
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{base_url}?{query_string}"

    links = [Link(rel="self", href=generate_url(page))]

    if total_pages > 0:
        links.append(Link(rel="first", href=generate_url(1)))
    if page > 1 and page <= total_pages:
        links.append(Link(rel="prev", href=generate_url(page - 1)))
    if page < total_pages:
        links.append(Link(rel="next", href=generate_url(page + 1)))
    if total_pages > 0 and page != total_pages:
        links.append(Link(rel="last", href=generate_url(total_pages)))
        
    return links

@app.get(
    "/api/history",
    response_model=HistoryResponse,
    summary="Endpoint de histórico (consultas, filtros, paginação e HATEOAS)",
    tags=["History"]
)
def get_history(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(DEFAULT_PAGE, ge=1),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=100),
    status: Optional[str] = Query(None),
    task: Optional[str] = Query(None),
    referencia: Optional[str] = Query(None),
    details: Optional[bool] = Query(DEFAULT_DETAILS),
):
    query = db.query(TaskHistory)
    
    if status:
        query = query.filter(TaskHistory.status == status.upper())
    if task:
        query = query.filter(TaskHistory.task == task.lower())
    if referencia:
        query = query.filter(TaskHistory.referencia.like(f"%{referencia}%"))

    total_items = query.count()
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
    
    if page > total_pages and total_items > 0:
        raise HTTPException(
            status_code=404, 
            detail=f"Página {page} não encontrada. O número máximo de páginas é {total_pages}."
        )

    offset = (page - 1) * limit
    items = query.order_by(TaskHistory.created_at.desc()).offset(offset).limit(limit).all()

    formatted_items: List[HistoryItemExpanded] = []
    for item in items:
        data_dict = item.to_dict(include_details=details)
        data_dict['created_at'] = item.created_at.isoformat() if item.created_at else None
        data_dict['finished_at'] = item.finished_at.isoformat() if item.finished_at else None
        if details and data_dict.get('details'):
            data_dict['details'] = format_number_in_dict(data_dict['details'])
        formatted_items.append(HistoryItemExpanded(**data_dict))

    links = build_pagination_links(request, total_pages, page, limit)

    return HistoryResponse(
        total_items=total_items,
        page=page,
        limit=limit,
        total_pages=total_pages,
        items=formatted_items,
        links=links
    )
