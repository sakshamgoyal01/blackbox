"""expand service catalog metadata

Revision ID: e3c3c646bcae
Revises: fe549dc6e5a5
Create Date: 2026-07-15 04:41:53.297585
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "e3c3c646bcae"
down_revision: Union[str, Sequence[str], None] = "fe549dc6e5a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "services",
        sa.Column(
            "description",
            sa.String(length=1000),
            nullable=True,
        ),
    )

    op.add_column(
        "services",
        sa.Column(
            "language",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "services",
        sa.Column(
            "framework",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "services",
        sa.Column(
            "deployment_type",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "services",
        sa.Column(
            "slack_channel",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "services",
        sa.Column(
            "runbook_url",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "services",
        sa.Column(
            "tags",
            postgresql.JSONB(),
            nullable=True,
        ),
    )


def downgrade() -> None:

    op.drop_column("services", "tags")
    op.drop_column("services", "runbook_url")
    op.drop_column("services", "slack_channel")
    op.drop_column("services", "deployment_type")
    op.drop_column("services", "framework")
    op.drop_column("services", "language")
    op.drop_column("services", "description")