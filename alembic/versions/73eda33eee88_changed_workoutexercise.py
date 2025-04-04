"""Changed WorkoutExercise

Revision ID: 73eda33eee88
Revises: 112225d56191
Create Date: 2025-02-16 11:26:47.189289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '73eda33eee88'
down_revision: Union[str, None] = '112225d56191'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout_exercise', sa.Column('rest_time_between', sa.Integer(), nullable=False))
    op.add_column('workout_exercise', sa.Column('rest_time_after', sa.Integer(), nullable=False))
    op.alter_column('workout_exercise', 'exercise_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('workout_exercise', 'sets',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.drop_column('workout_exercise', 'rest_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout_exercise', sa.Column('rest_time', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.alter_column('workout_exercise', 'sets',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('workout_exercise', 'exercise_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.drop_column('workout_exercise', 'rest_time_after')
    op.drop_column('workout_exercise', 'rest_time_between')
    # ### end Alembic commands ###
