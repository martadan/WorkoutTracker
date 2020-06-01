import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Workout, Exercise, WorkoutExercise


class WorkoutTestCase(unittest.TestCase):

    def setUp(self):
        """
        Define test variables and initialize app
        Has to be in this awkward camelCase to overload method in TestCase
        """
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = os.environ['HEROKU_POSTGRESQL_AQUA_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            self.db.create_all()

            # TODO populate tables with test values - this worked, but...
            # e1 = Exercise(
            #     name='kb swing',
            #     equipment='kettlebell',
            #     target='reps',
            #     link='dummy link'
            # )
            # e2 = Exercise(
            #     name='kb goblet squat',
            #     equipment='kettlebell',
            #     target='reps',
            #     link='another dummy link here'
            # )
            # e1.insert()
            # e2.insert()
            # w = Workout(
            #     name='test workout',
            #     focus='legs',
            #     repeat=False
            # )
            # w.insert()
            # m = WorkoutExercise(
            #     workout_id=1,#e1.id,
            #     exercise_id=1,#w.id,
            #     sets=3,
            #     reps=8,
            #     weight=4
            # )
            # m.insert()

    def tearDown(self):
        """
        Executed after each test
        Has to be in this awkward camelCase to overload method in TestCase
        """
        pass
        # TODO drop all tables so they're recreated in the setUp method - spent hours on this, still not working
        # with self.app.app_context():
        #     self.db.drop_all()
        #     # self.db.get_engine(self.app).dispose()

        # # delete all WorkoutExercise mappings
        # maps = WorkoutExercise.query.all()
        # for m in maps:
        #     m.delete()
        #
        # # delete all Exercises
        # exercises = Exercise.query.all()
        # for e in exercises:
        #     e.delete()
        #
        # # delete all Workouts
        # workouts = Workout.query.all()
        # for w in workouts:
        #     w.delete()

    def test_get_workouts(self):
        response = self.client().get('/workouts')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['workouts']), 1)

    # def test_get_exercises(self):
    #     response = self.client().get('/exercises')
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     # self.assertEqual(len(data['exercises']), 2)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
