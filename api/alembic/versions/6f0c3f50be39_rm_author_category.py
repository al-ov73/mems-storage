"""rm_author_category

Revision ID: 6f0c3f50be39
Revises: 7977bd4a2946
Create Date: 2024-12-13 23:33:12.065791+04:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6f0c3f50be39'
down_revision: Union[str, None] = '7977bd4a2946'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('memes_author_id_fkey', 'memes', type_='foreignkey')
    op.drop_column('memes', 'author_id')
    op.drop_column('memes', 'category')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memes', sa.Column('category', postgresql.ENUM('OTHER', 'CATS', 'PEOPLE', 'IT', name='categoryenum'), autoincrement=False, nullable=False))
    op.add_column('memes', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('memes_author_id_fkey', 'memes', 'users', ['author_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
