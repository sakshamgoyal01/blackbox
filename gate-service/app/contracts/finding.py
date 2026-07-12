from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class SourceTool(str, Enum):
    trivy = "trivy"
    gitleaks = "gitleaks"
    semgrep = "semgrep"
    syft = "syft"


class FindingCategory(str, Enum):
    secret = "secret"
    sast = "sast"
    sca = "sca"
    iac = "iac"
    container = "container"


class FindingSeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class FindingStatus(str, Enum):
    open = "open"
    fixed = "fixed"
    suppressed = "suppressed"
    false_positive = "false_positive"


class CanonicalFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    finding_id: UUID = Field(default_factory=uuid4)

    source_tool: SourceTool

    category: FindingCategory

    severity: FindingSeverity

    cve_id: str | None = None

    epss_score: float | None = None

    title: str

    description: str

    file_path: str | None = None

    line_number: int | None = None

    package_name: str | None = None

    package_version: str | None = None

    fixed_version: str | None = None

    service: str

    commit_sha: str

    environment: str

    detected_at: datetime

    status: FindingStatus = FindingStatus.open

    raw_scanner_output: dict[str, Any]