"""create posts table

Revision ID: 887b165bdd6f
Revises: 
Create Date: 2025-03-10 13:42:43.008122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '887b165bdd6f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", 
                    sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True, index=True),
                    sa.Column("title", sa.String(), nullable=False),
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
