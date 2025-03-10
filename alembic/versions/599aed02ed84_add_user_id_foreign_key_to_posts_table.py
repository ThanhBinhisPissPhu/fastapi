"""add user_id foreign key to posts table

Revision ID: 599aed02ed84
Revises: af5958161389
Create Date: 2025-03-10 13:57:08.499418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '599aed02ed84'
down_revision: Union[str, None] = 'af5958161389'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",
                  sa.Column("owner_id", sa.Integer(), nullable=False, index=True),
                  )
    op.create_foreign_key("posts_users_fk", 
                          source_table="posts", 
                          referent_table="users", 
                          local_cols=["owner_id"], 
                          remote_cols=["id"], 
                          ondelete="CASCADE"
                          )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
