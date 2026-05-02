"""add messages tabel

Revision ID: ad6efae210a1
Revises: 7997813abee9
Create Date: 2026-05-02 23:26:20.847883

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ad6efae210a1"
down_revision: Union[str, Sequence[str], None] = "7997813abee9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column("receiver_id", sa.Integer(), nullable=False),
        sa.Column("sender_email", sa.String(), nullable=False),
        sa.Column("receiver_email", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_messages")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("messages")
