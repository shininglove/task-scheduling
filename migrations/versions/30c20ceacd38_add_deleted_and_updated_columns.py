"""add deleted and updated columns

Revision ID: 30c20ceacd38
Revises: 
Create Date: 2025-01-07 08:12:18.725228

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "30c20ceacd38"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "taskitem",
        sa.Column("updated_at", sa.DateTime),
    )
    op.add_column("taskitem", sa.Column("deleted_at", sa.DateTime, nullable=True))
    op.add_column(
        "taskitem",
        sa.Column("mailable", sa.Boolean, server_default=sa.sql.true(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("taskitem", "updated_at")
    op.drop_column("taskitem", "deleted_at")
    op.drop_column("taskitem", "mailable")
