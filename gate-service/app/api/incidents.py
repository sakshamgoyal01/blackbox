from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.auth import verify_api_key

from app.contracts.incident import (
    IncidentCreate,
    IncidentDetailResponse,
    IncidentListResponse,
    IncidentResponse,
    IncidentUpdate,
)

from app.db.session import get_db

from app.services.incident_service import (
    create_incident_service,
    get_incident_service,
    list_incidents_service,
    update_incident_service,
)

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post(
    "",
    response_model=IncidentResponse,
    dependencies=[Depends(verify_api_key)],
)
def create_incident(
    request: IncidentCreate,
    db: Session = Depends(get_db),
):

    return create_incident_service(
        db,
        request,
    )


@router.get(
    "",
    response_model=IncidentListResponse,
    dependencies=[Depends(verify_api_key)],
)
def list_incidents(
    service: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):

    return {
        "incidents": list_incidents_service(
            db,
            service,
            status,
        )
    }


@router.get(
    "/{incident_id}",
    response_model=IncidentDetailResponse,
    dependencies=[Depends(verify_api_key)],
)
def get_incident(
    incident_id: UUID,
    db: Session = Depends(get_db),
):

    incident = get_incident_service(
        db,
        incident_id,
    )

    if incident is None:
        raise HTTPException(
            404,
            "Incident not found",
        )

    return incident


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
    dependencies=[Depends(verify_api_key)],
)
def update_incident(
    incident_id: UUID,
    request: IncidentUpdate,
    db: Session = Depends(get_db),
):

    incident = update_incident_service(
        db,
        incident_id,
        request,
    )

    if incident is None:
        raise HTTPException(
            404,
            "Incident not found",
        )

    return incident