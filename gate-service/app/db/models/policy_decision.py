import uuid
from datetime import datetime
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.database import Base


class PolicyDecision(Base):
    __tablename__ = "policy_decisions"

    __table_args__ = (
        Index(
            "idx_policy_service_commit",
            "service",
            "commit_sha",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    service: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    commit_sha: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    allowed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    violations: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    tier_at_decision: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    policy_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    policy_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    recommendation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    documentation_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    evaluated_resource: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    policy_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    decided_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    overridden: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    override_reason: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    override_approved_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    override_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )