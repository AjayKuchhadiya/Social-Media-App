"""Add created_at column

Revision ID: 29e0101b3e8c
Revises: 3894a232ce9d
Create Date: 2024-10-19 16:49:38.839332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision: str = '29e0101b3e8c'
down_revision: Union[str, None] = '3894a232ce9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    