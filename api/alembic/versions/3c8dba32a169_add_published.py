"""add_published

Revision ID: 3c8dba32a169
Revises: 9742bfbcea59
Create Date: 2024-12-20 22:28:12.828269+04:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3c8dba32a169"
down_revision: Union[str, None] = "9742bfbcea59"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "memes",
        sa.Column("published", sa.Boolean(), server_default=sa.text("'f'"), nullable=False),
    )
    op.execute("UPDATE memes SET published = 'f'")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("memes", "published")
    # ### end Alembic commands ###
