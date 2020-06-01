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
        """
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = os.environ['HEROKU_POSTGRESQL_AQUA_URL']
        # TODO look into testing.postgresql
        #  creates a temporary postgresql instance to test on instead of requiring a permanent database
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # populate tables with test values
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
            #     workout_id=1,
            #     exercise_id=1,
            #     sets=3,
            #     reps=8,
            #     weight=4
            # )
            # m.insert()

    def tearDown(self):
        """
        Executed after each test
        """
        pass

    def test_get_workouts(self):
        response = self.client().get('/workouts')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
