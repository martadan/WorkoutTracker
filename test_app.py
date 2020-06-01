import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, drop_db, Workout, Exercise, WorkoutExercise


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

            # populate tables with test values
            e1 = Exercise(
                name='kb swing',
                equipment='kettlebell',
                target='reps',
                link='dummy link'
            )
            e2 = Exercise(
                name='kb goblet squat',
                equipment='kettlebell',
                target='reps',
                link='another dummy link here'
            )
            e1.insert()
            e2.insert()
            w = Workout(
                name='test workout',
                focus='legs',
                repeat=False
            )
            w.insert()
            m = WorkoutExercise(
                workout_id=1,
                exercise_id=1,
                sets=3,
                reps=8,
                weight=4
            )
            m.insert()

    def tearDown(self):
        """
        Executed after each test
        Has to be in this awkward camelCase to overload method in TestCase
        """
        # drop all tables so they're recreated in the setUp method
        drop_db(self.app)

    def test_get_workouts(self):
        response = self.client().get('/workouts')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['workouts']), 1)

    def test_get_exercises(self):
        response = self.client().get('/exercises')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['exercises']), 2)

    def test_get_workout(self):
        response = self.client().get('/workouts/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['workout']['name'], 'test workout')

    def test_get_workout_404(self):
        response = self.client().get('/workouts/11')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_exercise(self):
        response = self.client().get('/exercises/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['exercise']['name'], 'kb swing')

    def test_get_exercise_404(self):
        response = self.client().get('/exercises/11')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_workout(self):
        workout = Workout(
            name='new workout',
            focus='upper',
            repeat=False
        )
        response = self.client().post(
            '/workouts',
            data=workout.format_short(),
            content_type='application/json'
        )
        data = json.loads(response.data)

        with self.app.app_context():
            matching_workouts = Workout.query.filter(Workout.name == workout.name).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(matching_workouts, 1)

    def test_create_workout_duplicate(self):
        workout = Workout(
            name='test workout',
            focus='upper',
            repeat=False
        )
        response = self.client().post(
            '/workouts',
            data=workout.format_short(),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_workout_malformed(self):
        workout = Workout(
            name='new workout',
            focus=False,
            repeat='wrong data type'
        )
        response = self.client().post(
            '/workouts',
            data=workout.format_short(),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_exercise(self):
        exercise = Exercise(
            name='bodyweight squat',
            equipment='bodyweight',
            target='reps',
            link='another link...'
        )
        response = self.client().post(
            '/exercises',
            data=exercise.format_short(),
            content_type='application/json'
        )
        data = json.loads(response.data)

        with self.app.app_context():
            matching_exercises = Exercise.query.filter(Exercise.name == exercise.name).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(matching_exercises, 1)

    def test_create_exercise_duplicate(self):
        exercise = Exercise(
            name='kb goblet squat',
            equipment='kettlebell',
            target='reps',
            link='another link...'
        )
        response = self.client().post(
            '/exercises',
            data=exercise.format_short(),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_exercise_malformed(self):
        exercise = Exercise(
            name='wrong data types',
            equipment=None,
            target=42,
            link=False
        )
        response = self.client().post(
            '/exercises',
            data=exercise.format_short(),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
