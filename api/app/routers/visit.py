from fastapi import APIRouter, Depends
from fastapi import Query, HTTPException
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_visit_repository
from ..models.visit import Visit
from ..schemas.visit import VisitInputSchema, VisitSchema
from ..utils.tasks import get_info_by_ip

router = APIRouter()

visit_repo = get_visit_repository()

@router.post("/", response_model=VisitSchema)
async def add_visit(
    visit_data: VisitInputSchema,
    db: Session = Depends(get_db),
) -> VisitSchema:
    visit_model = Visit.from_schema(visit_data)
    new_visit = await visit_repo.add_visit(visit_model, db)
    return new_visit


@router.get("/", response_model=list[VisitSchema])
async def get_last_visits(
        limit: int = Query(default=10, ge=1, le=100),
        db: Session = Depends(get_db),
) -> list[VisitSchema]:
    """
    Получить последние визиты с количеством посещений для каждого IP

    Параметры:
    - limit: количество возвращаемых записей (по умолчанию 10, максимум 100)
    """
    visits = await visit_repo.get_last_visits(db, limit)
    return visits


@router.post("/from-ip/", response_model=VisitSchema)
async def add_visit_from_ip(
        ip: str,
        db: Session = Depends(get_db),
) -> VisitSchema:
    """
    Добавить визит на основе IP-адреса (автоматически определяет геоданные)
    """
    visit_data = get_info_by_ip(ip)
    if not visit_data:
        raise HTTPException(status_code=400, detail="Не удалось определить данные по IP")

    new_visit = await visit_repo.add_visit(visit_data, db)
    return new_visit