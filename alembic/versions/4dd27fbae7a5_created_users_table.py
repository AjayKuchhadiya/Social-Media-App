"""Created users table

Revision ID: 4dd27fbae7a5
Revises: 29e0101b3e8c
Create Date: 2024-10-19 17:04:56.175186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision: str = '4dd27fbae7a5'
down_revision: Union[str, None] = '29e0101b3e8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   
    # Create 'users' table with 'id', 'email', 'password', and 'created_at' columns
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), unique=True, nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False)
    )


def downgrade() -> None:
    # Drop 'users' table
    op.drop_table('users')