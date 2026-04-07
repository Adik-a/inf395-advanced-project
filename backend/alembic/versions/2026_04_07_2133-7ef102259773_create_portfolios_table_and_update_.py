"""create portfolios table and update username column in users table

Revision ID: 7ef102259773
Revises: 8ead171d0b2c
Create Date: 2026-04-07 21:33:02.279883

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "7ef102259773"
down_revision: Union[str, Sequence[str], None] = "8ead171d0b2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "portfolios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_portfolios_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_portfolios")),
    )
    op.create_unique_constraint(
        op.f("uq_users_username"), "users", ["username"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("uq_users_username"), "users", type_="unique")
    op.drop_table("portfolios")
