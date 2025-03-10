"""add last few columns to posts table

Revision ID: 8674bf59f875
Revises: 599aed02ed84
Create Date: 2025-03-10 14:02:34.972622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8674bf59f875'
down_revision: Union[str, None] = '599aed02ed84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
