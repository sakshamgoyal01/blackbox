import enum
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    DateTime,
    Enum,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base


class IncidentSeverity(str, enum.Enum):
    sev1 = "sev1"
    sev2 = "sev2"
    sev3 = "sev3"
    sev4 = "sev4"


class IncidentStatus(str, enum.Enum):
    open = "open"
    investigating = "investigating"
    resolved = "resolved"

class IncidentType(str, enum.Enum):
    runtime = "runtime"
    vulnerability = "vulnerability"
    policy = "policy"
    deployment = "deployment"
    configuration = "configuration"
    other = "other"

class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    service: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    severity: Mapped[IncidentSeverity] = mapped_column(
        Enum(
            IncidentSeverity,
            name="incident_severity_enum",
        ),
        nullable=False,
    )

    status: Mapped[IncidentStatus] = mapped_column(
        Enum(
            IncidentStatus,
            name="incident_status_enum",
        ),
        nullable=False,
        default=IncidentStatus.open,
    )

    incident_type: Mapped[IncidentType] = mapped_column(
        Enum(
            IncidentType,
            name="incident_type_enum",
        ),
        nullable=False,
        default=IncidentType.runtime,
    )

    root_cause_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    tags: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    opened_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="manual",
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    postmortem: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    timeline = relationship(
        "IncidentTimelineEntry",
        back_populates="incident",
        cascade="all, delete-orphan",
    )