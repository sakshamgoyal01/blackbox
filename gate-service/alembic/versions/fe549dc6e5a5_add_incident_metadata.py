from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "fe549dc6e5a5"
down_revision = "89fb9074f669"
branch_labels = None
depends_on = None


incident_type_enum = postgresql.ENUM(
    "runtime",
    "security",
    "availability",
    "performance",
    name="incident_type_enum",
    create_type=False,
)


def upgrade():

    # Create PostgreSQL enum first
    incident_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "incidents",
        sa.Column(
            "incident_type",
            incident_type_enum,
            nullable=False,
            server_default="runtime",
        ),
    )

    op.add_column(
        "incidents",
        sa.Column(
            "root_cause_category",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "incidents",
        sa.Column(
            "tags",
            postgresql.JSONB(),
            nullable=True,
        ),
    )

    op.alter_column(
        "incidents",
        "incident_type",
        server_default=None,
    )


def downgrade():

    op.drop_column(
        "incidents",
        "tags",
    )

    op.drop_column(
        "incidents",
        "root_cause_category",
    )

    op.drop_column(
        "incidents",
        "incident_type",
    )

    incident_type_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )