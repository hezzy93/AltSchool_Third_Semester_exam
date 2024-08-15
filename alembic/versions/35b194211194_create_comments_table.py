"""Create comments table

Revision ID: <new_revision_id>
Revises: <previous_revision_id>
Create Date: <current_date>

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '<new_revision_id>'
down_revision: Union[str, None] = '<previous_revision_id>'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the comments table
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        # Add other columns as needed
    )


def downgrade() -> None:
    # Drop the comments table
    op.drop_table('comments')
