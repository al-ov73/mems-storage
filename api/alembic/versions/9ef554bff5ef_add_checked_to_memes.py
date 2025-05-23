"""add_checked_to_memes

Revision ID: 9ef554bff5ef
Revises: 3c8dba32a169
Create Date: 2024-12-27 10:45:48.445037+04:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ef554bff5ef"
down_revision: Union[str, None] = "3c8dba32a169"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "memes",
        sa.Column("checked", sa.Boolean(), server_default=sa.text("'t'"), nullable=False),
    )
    op.execute("UPDATE memes SET checked = TRUE")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("memes", "checked")
    # ### end Alembic commands ###
