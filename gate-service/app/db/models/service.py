import enum
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class CriticalityTier(str, enum.Enum):
    critical = "critical"
    standard = "standard"
    experimental = "experimental"


class Environment(str, enum.Enum):
    dev = "dev"
    prod = "prod"


class Service(Base):
    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    repo_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    owner: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    criticality_tier: Mapped[CriticalityTier] = mapped_column(
        Enum(CriticalityTier, name="criticality_tier_enum"),
        nullable=False,
    )

    environment: Mapped[Environment] = mapped_column(
        Enum(Environment, name="environment_enum"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    k8s_namespace: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    framework: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    deployment_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    slack_channel: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    runbook_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    tags: Mapped[list[str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )