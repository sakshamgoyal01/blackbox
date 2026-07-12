import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.database import Base


class FindingSource(str, enum.Enum):
    trivy = "trivy"
    gitleaks = "gitleaks"
    semgrep = "semgrep"
    syft = "syft"


class FindingCategory(str, enum.Enum):
    secret = "secret"
    sast = "sast"
    sca = "sca"
    iac = "iac"
    container = "container"


class FindingSeverity(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class FindingStatus(str, enum.Enum):
    open = "open"
    fixed = "fixed"
    suppressed = "suppressed"
    false_positive = "false_positive"


class Finding(Base):
    __tablename__ = "findings"

    __table_args__ = (
        Index("idx_findings_service", "service"),
        Index("idx_findings_commit_sha", "commit_sha"),
        Index("idx_findings_status", "status"),
        Index("idx_findings_severity", "severity"),
        Index(
            "idx_findings_service_commit",
            "service",
            "commit_sha",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    finding_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )

    source_tool: Mapped[FindingSource] = mapped_column(
        Enum(FindingSource, name="finding_source_enum"),
        nullable=False,
    )

    category: Mapped[FindingCategory] = mapped_column(
        Enum(FindingCategory, name="finding_category_enum"),
        nullable=False,
    )

    severity: Mapped[FindingSeverity] = mapped_column(
        Enum(FindingSeverity, name="finding_severity_enum"),
        nullable=False,
    )

    cve_id: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    epss_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    file_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    line_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    package_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    package_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    fixed_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    service: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    commit_sha: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    environment: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[FindingStatus] = mapped_column(
        Enum(FindingStatus, name="finding_status_enum"),
        nullable=False,
        default=FindingStatus.open,
    )

    raw_scanner_output: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )