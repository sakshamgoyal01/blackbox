from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Service
from app.db.session import get_db
from app.schemas import ServiceCreate, ServiceResponse
from app.auth import verify_api_key
router = APIRouter(tags=["Services"])


@router.post(
    "/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def register_service(
    payload: ServiceCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Service)
        .filter(Service.name == payload.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Service already exists.",
        )

    service = Service(
        name=payload.name,
        repo_url=str(payload.repo_url),
        owner=payload.owner,
        criticality_tier=payload.criticality_tier,
        environment=payload.environment,
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


@router.get(
    "/services/{name}",
    response_model=ServiceResponse,
    dependencies=[Depends(verify_api_key)],
)
def get_service(
    name: str,
    db: Session = Depends(get_db),
):
    service = (
        db.query(Service)
        .filter(Service.name == name)
        .first()
    )

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found.",
        )

    return service