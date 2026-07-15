"""add runtime event metadata

Revision ID: 89fb9074f669
Revises: d3ca0e8531c5
Create Date: 2026-07-15 03:31:46.301085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89fb9074f669'
down_revision: Union[str, Sequence[str], None] = 'd3ca0e8531c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "runtime_events",
        sa.Column(
            "rule_url",
            sa.String(length=1000),
            nullable=True,
        ),
    )

    op.add_column(
        "runtime_events",
        sa.Column(
            "mitre_attack",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "runtime_events",
        sa.Column(
            "remediation_summary",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "runtime_events",
        sa.Column(
            "investigation_notes",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade():

    op.drop_column(
        "runtime_events",
        "investigation_notes",
    )

    op.drop_column(
        "runtime_events",
        "remediation_summary",
    )

    op.drop_column(
        "runtime_events",
        "mitre_attack",
    )

    op.drop_column(
        "runtime_events",
        "rule_url",
    )