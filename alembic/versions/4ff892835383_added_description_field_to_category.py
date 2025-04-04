"""Added description field to Category

Revision ID: 4ff892835383
Revises: 667f4a5ee259
Create Date: 2025-02-11 14:47:45.297470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ff892835383'
down_revision: Union[str, None] = '667f4a5ee259'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'description')
    # ### end Alembic commands ###
