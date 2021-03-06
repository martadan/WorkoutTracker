"""empty message

Revision ID: ec2f315463aa
Revises: 8721d93a364e
Create Date: 2020-05-31 18:35:24.942255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec2f315463aa'
down_revision = '8721d93a364e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        'WorkoutExercises_workout_id_fkey',
        'WorkoutExercises',
        'Workouts',
        ['workout_id'],
        ['id']
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        'WorkoutExercises_workout_id_fkey',
        'WorkoutExercises',
        type_='foreignkey'
    )
    # ### end Alembic commands ###
