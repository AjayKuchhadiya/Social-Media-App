"""Create posts table

Revision ID: 3894a232ce9d
Revises: 
Create Date: 2024-10-19 16:30:25.061660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3894a232ce9d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create 'posts' table with 'id', 'title', 'content' columns
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text, nullable=False)
    )


def downgrade() -> None:
    # Drop 'posts' table
    op.drop_table('posts')