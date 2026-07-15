"""add scanner metadata to findings

Revision ID: d3ca0e8531c5
Revises: 38f2720323e8
Create Date: 2026-07-15 03:24:22.072728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3ca0e8531c5'
down_revision: Union[str, Sequence[str], None] = '38f2720323e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "findings",
        sa.Column(
            "scanner_url",
            sa.String(length=1000),
            nullable=True,
        ),
    )

    op.add_column(
        "findings",
        sa.Column(
            "remediation_summary",
            sa.Text(),
            nullable=True,
        ),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "findings",
        "remediation_summary",
    )

    op.drop_column(
        "findings",
        "scanner_url",
    )
    pass
