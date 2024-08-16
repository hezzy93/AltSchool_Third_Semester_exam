"""Change rating column to Integer

Revision ID: fed1c1a16490
Revises: 46b1161fa70e
Create Date: 2024-08-13 22:29:18.856655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fed1c1a16490'
down_revision: Union[str, None] = '46b1161fa70e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE ratings ALTER COLUMN rating TYPE INTEGER USING rating::integer')


def downgrade() -> None:
    op.execute('ALTER TABLE ratings ALTER COLUMN rating TYPE VARCHAR USING rating::VARCHAR')
