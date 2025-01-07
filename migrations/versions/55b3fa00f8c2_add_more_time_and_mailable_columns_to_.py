"""add more time and mailable columns to descriptions

Revision ID: 55b3fa00f8c2
Revises: 30c20ceacd38
Create Date: 2025-01-07 08:56:30.229174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55b3fa00f8c2'
down_revision: Union[str, None] = '30c20ceacd38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "taskdescription",
        sa.Column("updated_at", sa.DateTime),
    )
    op.add_column("taskdescription", sa.Column("deleted_at", sa.DateTime, nullable=True))
    op.add_column(
        "taskdescription",
        sa.Column("mailable", sa.Boolean, server_default=sa.sql.true(), nullable=False),
    )



def downgrade() -> None:
    op.drop_column("taskdescription", "updated_at")
    op.drop_column("taskdescription", "deleted_at")
    op.drop_column("taskdescription", "mailable")
