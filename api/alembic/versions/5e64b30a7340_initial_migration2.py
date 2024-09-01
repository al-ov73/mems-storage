"""initial migration2

Revision ID: 5e64b30a7340
Revises: 7e22104520f9
Create Date: 2024-09-01 23:41:08.772889+04:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e64b30a7340'
down_revision: Union[str, None] = '7e22104520f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memes', sa.Column('label_id', sa.Integer(), nullable=True))
    op.add_column('memes', sa.Column('comment_id', sa.Integer(), nullable=True))
    op.add_column('memes', sa.Column('like_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'memes', 'comments', ['comment_id'], ['id'])
    op.create_foreign_key(None, 'memes', 'labels', ['label_id'], ['id'])
    op.create_foreign_key(None, 'memes', 'likes', ['like_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'memes', type_='foreignkey')
    op.drop_constraint(None, 'memes', type_='foreignkey')
    op.drop_constraint(None, 'memes', type_='foreignkey')
    op.drop_column('memes', 'like_id')
    op.drop_column('memes', 'comment_id')
    op.drop_column('memes', 'label_id')
    # ### end Alembic commands ###
