"""Add measurement_method enum

Revision ID: 7bb6f8f3518d
Revises: 0313ac066b9f
Create Date: 2025-04-06 10:28:26.268926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7bb6f8f3518d'
down_revision: Union[str, None] = '0313ac066b9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('challenges', 'measurement_method',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.Enum('DOWN_UP', 'PROXIMITY', 'STILLNESS', name='measurement_method_enum'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('challenges', 'measurement_method',
               existing_type=sa.Enum('DOWN_UP', 'PROXIMITY', 'STILLNESS', name='measurement_method_enum'),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###
