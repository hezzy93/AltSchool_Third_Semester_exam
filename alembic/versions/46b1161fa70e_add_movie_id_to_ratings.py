"""Add movie_id to ratings

Revision ID: 46b1161fa70e
Revises: ccb4db327ca8
Create Date: 2024-07-24 00:02:35.977615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46b1161fa70e'
down_revision: Union[str, None] = 'ccb4db327ca8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ratings', sa.Column('movie_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ratings', 'movies', ['movie_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.drop_column('ratings', 'movie_id')
