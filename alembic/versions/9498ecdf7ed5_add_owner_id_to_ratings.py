"""Add owner_id to ratings

Revision ID: 9498ecdf7ed5
Revises: fed1c1a16490
Create Date: 2024-07-23 23:58:15.242100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9498ecdf7ed5'
down_revision: Union[str, None] = 'fed1c1a16490'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ratings', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ratings', 'users', ['owner_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.drop_column('ratings', 'owner_id')
