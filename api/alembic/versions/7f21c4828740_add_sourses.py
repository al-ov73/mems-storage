"""add_sourses

Revision ID: 7f21c4828740
Revises: 5e52cab7336c
Create Date: 2024-12-15 00:08:55.620155+04:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7f21c4828740"
down_revision: Union[str, None] = "5e52cab7336c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("memes", sa.Column("source_name", sa.String(), nullable=False))
    op.add_column("memes", sa.Column("source_type", sa.String(), nullable=False))
    op.drop_constraint("memes_name_key", "memes", type_="unique")
    op.drop_column("memes", "name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("memes", sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint("memes_name_key", "memes", ["name"])
    op.drop_column("memes", "source_type")
    op.drop_column("memes", "source_name")
    # ### end Alembic commands ###
