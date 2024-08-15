"""Create comments table

Revision ID: 35b194211194
Revises: fed1c1a16490
Create Date: 2024-08-16 00:11:14.418478

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '35b194211194'
down_revision: Union[str, None] = 'fed1c1a16490'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('comment', sa.String(), nullable=False),
        sa.Column('movie_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id']),
    )

def downgrade() -> None:
    op.drop_table('comments')
