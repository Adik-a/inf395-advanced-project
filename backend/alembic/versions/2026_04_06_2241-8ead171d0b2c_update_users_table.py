"""update users table

Revision ID: 8ead171d0b2c
Revises: b0da7ade568d
Create Date: 2026-04-06 22:41:24.135772

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8ead171d0b2c"
down_revision: Union[str, Sequence[str], None] = "b0da7ade568d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("email", sa.String(), nullable=False))
    op.add_column(
        "users", sa.Column("first_name", sa.String(), nullable=False)
    )
    op.add_column("users", sa.Column("last_name", sa.String(), nullable=True))
    op.add_column("users", sa.Column("bio", sa.String(), nullable=True))
    op.add_column("users", sa.Column("rating", sa.Float(), nullable=False))
    op.add_column("users", sa.Column("is_oauth", sa.Boolean(), nullable=False))
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.alter_column(
        "users", "username", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "users", "password", existing_type=sa.VARCHAR(), nullable=True
    )
    op.drop_constraint(op.f("uq_users_username"), "users", type_="unique")
    op.create_unique_constraint(op.f("uq_users_email"), "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("uq_users_email"), "users", type_="unique")
    op.create_unique_constraint(
        op.f("uq_users_username"),
        "users",
        ["username"],
        postgresql_nulls_not_distinct=False,
    )
    op.alter_column(
        "users", "password", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "users", "username", existing_type=sa.VARCHAR(), nullable=False
    )
    op.drop_column("users", "created_at")
    op.drop_column("users", "is_oauth")
    op.drop_column("users", "rating")
    op.drop_column("users", "bio")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
    op.drop_column("users", "email")
