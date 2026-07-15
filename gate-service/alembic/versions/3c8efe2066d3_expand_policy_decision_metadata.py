from alembic import op

"""expand policy decision metadata"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "3c8efe2066d3"
down_revision: Union[str, Sequence[str], None] = "e3c3c646bcae"
branch_labels = None
depends_on = None

def upgrade():

    op.add_column(
        "policy_decisions",
        sa.Column(
            "policy_name",
            sa.String(255),
            nullable=True,
        ),
    )

    op.add_column(
        "policy_decisions",
        sa.Column(
            "policy_description",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "policy_decisions",
        sa.Column(
            "recommendation",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "policy_decisions",
        sa.Column(
            "documentation_url",
            sa.String(1000),
            nullable=True,
        ),
    )

    op.add_column(
        "policy_decisions",
        sa.Column(
            "evaluated_resource",
            sa.String(255),
            nullable=True,
        ),
    )

    op.add_column(
        "policy_decisions",
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade():

    op.drop_column("policy_decisions", "metadata")
    op.drop_column("policy_decisions", "evaluated_resource")
    op.drop_column("policy_decisions", "documentation_url")
    op.drop_column("policy_decisions", "recommendation")
    op.drop_column("policy_decisions", "policy_description")
    op.drop_column("policy_decisions", "policy_name")