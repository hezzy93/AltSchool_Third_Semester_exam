"""Remove is_active column from users table

Revision ID: ccb4db327ca8
Revises: e50fbe6904c8
Create Date: 2024-07-21 00:48:36.228727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccb4db327ca8'
down_revision: Union[str, None] = 'e50fbe6904c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'is_active')


def downgrade() -> None:
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
