"""empty message

Revision ID: c7befdc5c7f8
Revises: ec2f315463aa
Create Date: 2020-05-31 19:29:25.222322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7befdc5c7f8'
down_revision = 'ec2f315463aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        'WorkoutExercises_exercise_id_fkey',
        'WorkoutExercises',
        'Exercises',
        ['exercise_id'],
        ['id']
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        'WorkoutExercises_exercise_id_fkey',
        'WorkoutExercises',
        type_='foreignkey'
    )
    # ### end Alembic commands ###
