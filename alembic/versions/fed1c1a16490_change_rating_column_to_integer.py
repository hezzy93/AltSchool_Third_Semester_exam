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
    # Change the rating column type to INTEGER with explicit casting
    op.execute('ALTER TABLE ratings ALTER COLUMN rating TYPE INTEGER USING rating::integer')

    # Perform other schema changes
    op.alter_column('comments', 'comment',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('comments', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('comments', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_index(op.f('ix_comments_comment'), 'comments', ['comment'], unique=False)
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    
    # Indexes related to ratings
    op.create_index(op.f('ix_ratings_rating'), 'ratings', ['rating'], unique=False)
    
    # Index changes
    op.drop_index('ix_users_user_name', table_name='users')
    op.create_index(op.f('ix_users_user_name'), 'users', ['user_name'], unique=True)


def downgrade() -> None:
    # Revert the rating column type to VARCHAR with explicit casting
    op.execute('ALTER TABLE ratings ALTER COLUMN rating TYPE VARCHAR USING rating::VARCHAR')

    # Revert other schema changes
    op.drop_index(op.f('ix_users_user_name'), table_name='users')
    op.create_index('ix_users_user_name', 'users', ['user_name'], unique=False)
    op.drop_index(op.f('ix_ratings_rating'), table_name='ratings')
    
    op.alter_column('comments', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'comment',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_comment'), table_name='comments')
