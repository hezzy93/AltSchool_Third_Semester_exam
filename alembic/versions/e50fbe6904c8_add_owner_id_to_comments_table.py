"""Add owner_id to comments

Revision ID: e50fbe6904c8
Revises: 7c3f6d8e2052
Create Date: 2024-07-23 23:01:44.231733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e50fbe6904c8'
down_revision: Union[str, None] = '7c3f6d8e2052'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('comments', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'users', ['owner_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'owner_id')
