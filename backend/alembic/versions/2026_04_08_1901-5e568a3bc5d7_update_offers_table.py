"""update offers table

Revision ID: 5e568a3bc5d7
Revises: f2e8baa210f7
Create Date: 2026-04-08 19:01:59.809054

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "5e568a3bc5d7"
down_revision: Union[str, Sequence[str], None] = "f2e8baa210f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        op.f("uq_offers_user_id_job_id"), "offers", ["user_id", "job_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("uq_offers_user_id_job_id"), "offers", type_="unique"
    )
