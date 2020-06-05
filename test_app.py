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
        drop_db()

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
        workout_string = json.dumps({
            'name': 'new workout',
            'focus': 'upper',
            'repeat': False
        })
        response = self.client().post(
            '/workouts',
            data=workout_string,
            content_type='application/json'
        )
        data = json.loads(response.data)

        with self.app.app_context():
            matching_workouts = Workout.query.filter(Workout.name == 'new workout').count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(matching_workouts, 1)

    def test_create_workout_with_exercises(self):
        full_workout_string = json.dumps({
            'name': 'new workout',
            'focus': 'upper',
            'repeat': False,
            'exercises': [
                {
                    'name': 'kb swing',
                    'sets': 5,
                    'reps': 20,
                    'weight': 40
                },
                {
                    'name': 'kb goblet squat',
                    'sets': 1,
                    'reps': 15,
                    'weight': 40
                }
            ]
        })
        response = self.client().post(
            '/workouts',
            data=full_workout_string,
            content_type='application/json'
        )
        data = json.loads(response.data)

        with self.app.app_context():
            matching_workouts = Workout.query.filter(Workout.name == 'new workout').count()
            matching_exercises = len(Workout.query.filter(Workout.name == 'new workout').first().exercises)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(matching_workouts, 1)
        self.assertEqual(matching_exercises, 2)

    def test_create_workout_duplicate(self):
        workout_string = json.dumps({
            'name': 'test workout',
            'focus': 'upper',
            'repeat': False
        })
        response = self.client().post(
            '/workouts',
            data=workout_string,
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_workout_malformed(self):
        workout_string = json.dumps({
            'name': 'bad workout',
            'focus': False,
            'repeat': 'wrong data type'
        })
        response = self.client().post(
            '/workouts',
            data=workout_string,
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_workout_incorrect_exercise(self):
        full_workout_string = json.dumps({
            'name': 'new workout',
            'focus': 'upper',
            'repeat': False,
            'exercises': [
                {
                    'name': 'not a workout',
                    'sets': 1,
                    'reps': 1,
                    'weight': 5
                }
            ]
        })
        response = self.client().post(
            '/workouts',
            data=full_workout_string,
            content_type='application/json'
        )
        data = json.loads(response.data)

        with self.app.app_context():
            matching_workouts = Workout.query.filter(Workout.name == 'new workout').count()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(matching_workouts, 0)

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

    def test_delete_workout(self):
        response = self.client().delete('/workouts/1')
        data = json.loads(response.data)

        with self.app.app_context():
            matching_workout = Workout.query.get(1)
            matching_mappings = WorkoutExercise.query.filter(WorkoutExercise.workout_id == 1).count()
            matching_exercise = Exercise.query.get(1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['workout_id'], 1)
        self.assertIsNone(matching_workout)
        self.assertEqual(matching_mappings, 0)
        self.assertIsNotNone(matching_exercise)  # do not want exercise itself deleted

    def test_delete_workout_out_of_bounds(self):
        response = self.client().delete('/workouts/11')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_exercise(self):
        response = self.client().delete('/exercises/2')
        data = json.loads(response.data)

        with self.app.app_context():
            matching_exercise = Exercise.query.get(2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['exercise_id'], 2)
        self.assertIsNone(matching_exercise)

    def test_delete_exercise_out_of_bound(self):
        response = self.client().delete('/exercises/11')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_exercise_in_use(self):
        response = self.client().delete('/exercises/1')
        data = json.loads(response.data)

        with self.app.app_context():
            matching_exercise = Exercise.query.get(1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertIsNotNone(matching_exercise)

    # TODO add additional tests for:
    #   patch to Exercise and Workout
    #   RBAC


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
