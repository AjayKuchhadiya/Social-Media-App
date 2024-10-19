"""Add foreign key to post table

Revision ID: 229692a18f9b
Revises: 4dd27fbae7a5
Create Date: 2024-10-19 17:10:28.439518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '229692a18f9b'
down_revision: Union[str, None] = '4dd27fbae7a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'user_id' column to 'posts' table, with a foreign key reference to 'users.id'
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_user_id',  # Name of the foreign key constraint
        'posts',       # Source table (posts)
        'users',       # Target table (users)
        ['user_id'],   # Source column in posts
        ['id'],         # Target column in users
    )


def downgrade() -> None:
    # Remove the foreign key and 'user_id' column
    op.drop_constraint('fk_user_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')