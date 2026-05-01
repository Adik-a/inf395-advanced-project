"""update profiles table and add faqs, requirements table

Revision ID: 7997813abee9
Revises: 5e568a3bc5d7
Create Date: 2026-05-01 23:39:49.196046

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "7997813abee9"
down_revision: Union[str, Sequence[str], None] = "5e568a3bc5d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "faqs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question", sa.String(), nullable=False),
        sa.Column("answer", sa.String(), nullable=False),
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
            name=op.f("fk_faqs_portfolio_id_portfolios"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_faqs")),
    )
    op.create_table(
        "requirements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("requirement", sa.String(), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
            name=op.f("fk_requirements_portfolio_id_portfolios"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_requirements")),
    )
    op.add_column(
        "portfolios", sa.Column("category", sa.String(), nullable=False)
    )
    op.add_column(
        "portfolios", sa.Column("subcategory", sa.String(), nullable=False)
    )
    op.add_column(
        "portfolios", sa.Column("initial_status", sa.String(), nullable=False)
    )
    op.add_column(
        "portfolios", sa.Column("tags", sa.ARRAY(sa.String()), nullable=False)
    )
    op.add_column(
        "portfolios", sa.Column("pricing_mode", sa.String(), nullable=False)
    )
    op.add_column(
        "portfolios", sa.Column("price_basic", sa.Integer(), nullable=False)
    )
    op.add_column(
        "portfolios", sa.Column("price_standard", sa.Integer(), nullable=True)
    )
    op.add_column(
        "portfolios", sa.Column("price_premium", sa.Integer(), nullable=True)
    )
    op.add_column(
        "portfolios",
        sa.Column("package_name_basic", sa.String(), nullable=False),
    )
    op.add_column(
        "portfolios",
        sa.Column("package_name_standard", sa.String(), nullable=True),
    )
    op.add_column(
        "portfolios",
        sa.Column("package_name_premium", sa.String(), nullable=True),
    )
    op.add_column(
        "portfolios",
        sa.Column("description_basic", sa.String(), nullable=False),
    )
    op.add_column(
        "portfolios",
        sa.Column("description_standard", sa.String(), nullable=True),
    )
    op.add_column(
        "portfolios",
        sa.Column("description_premium", sa.String(), nullable=True),
    )
    op.add_column(
        "portfolios", sa.Column("delivery_basic", sa.String(), nullable=False)
    )
    op.add_column(
        "portfolios",
        sa.Column("delivery_standard", sa.String(), nullable=True),
    )
    op.add_column(
        "portfolios", sa.Column("delivery_premium", sa.String(), nullable=True)
    )
    op.add_column(
        "portfolios", sa.Column("revisions_basic", sa.String(), nullable=False)
    )
    op.add_column(
        "portfolios",
        sa.Column("revisions_standard", sa.String(), nullable=True),
    )
    op.add_column(
        "portfolios",
        sa.Column("revisions_premium", sa.String(), nullable=True),
    )
    op.add_column(
        "portfolios",
        sa.Column("images", sa.ARRAY(sa.String()), nullable=False),
    )
    op.drop_column("portfolios", "price")
    op.drop_column("portfolios", "rating")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "portfolios",
        sa.Column(
            "rating",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "portfolios",
        sa.Column(
            "price",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("portfolios", "images")
    op.drop_column("portfolios", "revisions_premium")
    op.drop_column("portfolios", "revisions_standard")
    op.drop_column("portfolios", "revisions_basic")
    op.drop_column("portfolios", "delivery_premium")
    op.drop_column("portfolios", "delivery_standard")
    op.drop_column("portfolios", "delivery_basic")
    op.drop_column("portfolios", "description_premium")
    op.drop_column("portfolios", "description_standard")
    op.drop_column("portfolios", "description_basic")
    op.drop_column("portfolios", "package_name_premium")
    op.drop_column("portfolios", "package_name_standard")
    op.drop_column("portfolios", "package_name_basic")
    op.drop_column("portfolios", "price_premium")
    op.drop_column("portfolios", "price_standard")
    op.drop_column("portfolios", "price_basic")
    op.drop_column("portfolios", "pricing_mode")
    op.drop_column("portfolios", "tags")
    op.drop_column("portfolios", "initial_status")
    op.drop_column("portfolios", "subcategory")
    op.drop_column("portfolios", "category")
    op.drop_table("requirements")
    op.drop_table("faqs")
