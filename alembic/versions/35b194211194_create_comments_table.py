"""Add movie_id column to comments table

Revision ID: 7c3f6d8e2052
Revises: 35b194211194
Create Date: 2024-07-14 23:52:12.630561

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7c3f6d8e2052'
down_revision: Union[str, None] = '35b194211194'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('comments', sa.Column('movie_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'movies', ['movie_id'], ['id'])

def downgrade() -> None:
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'movie_id')
