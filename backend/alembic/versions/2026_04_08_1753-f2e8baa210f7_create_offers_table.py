"""create offers table

Revision ID: f2e8baa210f7
Revises: 02787008bc80
Create Date: 2026-04-08 17:53:31.510764

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f2e8baa210f7"
down_revision: Union[str, Sequence[str], None] = "02787008bc80"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "offers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("letter", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["job_id"], ["jobs.id"], name=op.f("fk_offers_job_id_jobs")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_offers_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_offers")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("offers")
