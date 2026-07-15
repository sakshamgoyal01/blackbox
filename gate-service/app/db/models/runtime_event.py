import enum
import uuid
from sqlalchemy import Text
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class RuntimeEventStatus(str, enum.Enum):

    open = "open"

    acknowledged = "acknowledged"

    false_positive = "false_positive"


class RuntimeEvent(Base):

    __tablename__ = "runtime_events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    rule = Column(
        String(255),
        nullable=False,
    )

    priority = Column(
        String(30),
        nullable=False,
    )

    output = Column(
        Text,
        nullable=False,
    )

    container_id = Column(
        String(128),
    )

    container_name = Column(
        String(255),
    )

    pod_name = Column(
        String(255),
    )

    namespace = Column(
        String(255),
    )

    node = Column(
        String(255),
    )

    k8s_labels = Column(
        JSONB,
    )

    service = Column(
        String(100),
    )

    source = Column(
        String(30),
        nullable=False,
        default="falco",
    )
    rule_url = Column(
        String(1000),
        nullable=True,
    )

    mitre_attack = Column(
        String(255),
        nullable=True,
    )

    remediation_summary = Column(
        Text,
        nullable=True,
    )

    investigation_notes = Column(
        Text,
        nullable=True,
    )

    raw_output = Column(
        JSONB,
        nullable=False,
    )

    detected_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    status = Column(
        Enum(RuntimeEventStatus, name="runtime_event_status_enum",),
        nullable=False,
        default=RuntimeEventStatus.open,
    )