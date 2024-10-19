"""Add CASCADE to f_key in posts table

Revision ID: c78c724f844c
Revises: 229692a18f9b
Create Date: 2024-10-19 17:16:55.189257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c78c724f844c'
down_revision: Union[str, None] = '229692a18f9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing foreign key constraint
    op.drop_constraint('fk_user_id', 'posts', type_='foreignkey')
    
    # Create a new foreign key constraint with ON DELETE CASCADE
    op.create_foreign_key(
        'fk_user_id',   # Name of the foreign key constraint
        'posts',        # Source table (posts)
        'users',        # Target table (users)
        ['user_id'],    # Source column in posts
        ['id'],         # Target column in users
        ondelete='CASCADE'  # Add the ON DELETE CASCADE behavior
    )


def downgrade() -> None:
    # Drop the foreign key with CASCADE
    op.drop_constraint('fk_user_id', 'posts', type_='foreignkey')
    
    # Recreate the original foreign key without CASCADE
    op.create_foreign_key(
        'fk_user_id',   # Name of the foreign key constraint
        'posts',        # Source table (posts)
        'users',        # Target table (users)
        ['user_id'],    # Source column in posts
        ['id']          # Target column in users
    )