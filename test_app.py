import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, drop_db, Workout, Exercise, WorkoutExercise

ATHLETE_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFKOW9HX3R5eHlHcG1Ub1ZVNlRSTiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNDUyOXU3Mi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZTQ3MTQxNTJlODYwMDE5YTViM2NkIiwiYXVkIjoid29ya291dCIsImlhdCI6MTU5MTY1NDIwMCwiZXhwIjoxNTkxNjYxMzk5LCJhenAiOiJhYlF0cjlxeFJzdUl6MWdicjlHZlhFUENIYmNnS29GbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmV4ZXJjaXNlIiwiZ2V0OndvcmtvdXQiLCJwYXRjaDp3b3Jrb3V0IiwicG9zdDp3b3Jrb3V0Il19.uhVKtMDCn3vvnkUVIWKQutTjdXB5TBXAGMMuM7wk-_zv4jmRYH2rRh4tbrlY0jPkGklmTfLapQBLYcHw1sagCQiMJXY5EQY72uLwToMI8qz-22jLeu1u8E3xtkLrcoX3PWmhIBncpgS5vwPhfyE7ntXlHbEEk6vUHoaVCbbfQkhx8hPV2j3I8LOMx27C3_2i8WWrEsQCe5d2xkfFdllbA3ctePuju1Pk7s81V6IMoldvVc4bUFOH2khBfkxQ0Ov0UbXBlXe1edsKrEzZ9yttDlJ5sxpuOyXygnYUvBGNk2jMyPBBhirVJnBW4KUEljHDQctk7cZRksqALgGWmZTdFA'
ATHLETE_HEADER = {'Authorization': f'Bearer {ATHLETE_TOKEN}'}
COACH_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFKOW9HX3R5eHlHcG1Ub1ZVNlRSTiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNDUyOXU3Mi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVkZTQ1YWIxNTJlODYwMDE5YTViMTQxIiwiYXVkIjoid29ya291dCIsImlhdCI6MTU5MTY1NDI2NywiZXhwIjoxNTkxNjYxNDY2LCJhenAiOiJhYlF0cjlxeFJzdUl6MWdicjlHZlhFUENIYmNnS29GbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmV4ZXJjaXNlIiwiZGVsZXRlOndvcmtvdXQiLCJnZXQ6ZXhlcmNpc2UiLCJnZXQ6d29ya291dCIsInBhdGNoOmV4ZXJjaXNlIiwicGF0Y2g6d29ya291dCIsInBvc3Q6ZXhlcmNpc2UiLCJwb3N0OndvcmtvdXQiXX0.rbFCbBqFpl3jPAnqwNmXYPR5cUSGIA1NZu8txnJ19mNA2mUl5Py14z-2N_sXS3IkrRT0HLofnDA1ndfG3-R87dM44pOZ6-Jwp9UiGKpo7CZu5ZylykaSAjq8nf2jpKyEO8hmsSnAHi24CuVGNVcipk5N6QBa9v18hQe5xJ7dBvrkbT1xgx3pso0nLmiz9lDlCSlFnJ7isMbLdWaieQiyYM7Z8nAIjYT4f7ckR2OAEBAg9acjFN_H1uIuha2Tdd0uVt1Ed6vMcixEkJN73sh0KQ2TKjrAJWzMa-KDHspRlOA4V286lOEvbuJRsrX-_sij_4BcKXV7A2AAKJdViLs4VA'
COACH_HEADER = {'Authorization': f'Bearer {COACH_TOKEN}'}


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
        response = self.client().get('/workouts', headers=ATHLETE_HEADER)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['workouts']), 1)

    def test_get_exercises(self):
        response = self.client().get('/exercises', headers=ATHLETE_HEADER)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['exercises']), 2)

    def test_get_workout(self):
        response = self.client().get('/workouts/1', headers=ATHLETE_HEADER)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['workout']['name'], 'test workout')

    def test_get_workout_404(self):
        response = self.client().get('/workouts/11', headers=ATHLETE_HEADER)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_exercise(self):
        response = self.client().get('/exercises/1', headers=ATHLETE_HEADER)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['exercise']['name'], 'kb swing')

    def test_get_exercise_404(self):
        response = self.client().get('/exercises/11', headers=ATHLETE_HEADER)
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
            content_type='application/json',
            headers=ATHLETE_HEADER
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
            content_type='application/json',
            headers=ATHLETE_HEADER
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
            content_type='application/json',
            headers=ATHLETE_HEADER
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
            content_type='application/json',
            headers=ATHLETE_HEADER
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
            content_type='application/json',
            headers=ATHLETE_HEADER
        )
        data = json.loads(response.data)

        with self.app.app_context():
            matching_workouts = Workout.query.filter(Workout.name == 'new workout').count()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(matching_workouts, 0)

    def test_create_exercise(self):
        exercise_string = json.dumps({
            'name': 'bodyweight squat',
            'equipment': 'bodyweight',
            'target': 'reps',
            'link': 'another link...'
        })
        response = self.client().post(
            '/exercises',
            data=exercise_string,
            content_type='application/json',
            headers=COACH_HEADER
        )
        data = json.loads(response.data)

        with self.app.app_context():
            matching_exercises = Exercise.query.filter(Exercise.name == 'bodyweight squat').count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(matching_exercises, 1)

    def test_create_exercise_duplicate(self):
        exercise_string = json.dumps({
            'name': 'kb goblet squat',
            'equipment': 'kettlebell',
            'target': 'reps',
            'link': 'another link...'
        })
        response = self.client().post(
            '/exercises',
            data=exercise_string,
            content_type='application/json',
            headers=COACH_HEADER
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_exercise_malformed(self):
        exercise_string = json.dumps({
            'name': 'wrong data types',
            'equipment': None,
            'target': 42,
            'link': False
        })
        response = self.client().post(
            '/exercises',
            data=exercise_string,
            content_type='application/json',
            headers=COACH_HEADER
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_workout(self):
        response = self.client().delete('/workouts/1', headers=COACH_HEADER)
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
        response = self.client().delete('/workouts/11', headers=COACH_HEADER)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_exercise(self):
        response = self.client().delete('/exercises/2', headers=COACH_HEADER)
        data = json.loads(response.data)

        with self.app.app_context():
            matching_exercise = Exercise.query.get(2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['exercise_id'], 2)
        self.assertIsNone(matching_exercise)

    def test_delete_exercise_out_of_bound(self):
        response = self.client().delete('/exercises/11', headers=COACH_HEADER)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_exercise_in_use(self):
        response = self.client().delete('/exercises/1', headers=COACH_HEADER)
        data = json.loads(response.data)

        with self.app.app_context():
            matching_exercise = Exercise.query.get(1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertIsNotNone(matching_exercise)

    def test_update_workout(self):
        full_workout_string = json.dumps({
            'name': 'updated workout',
            'focus': 'upper',
            'repeat': False,
            'exercises': [
                {
                    'name': 'kb goblet squat',
                    'sets': 4,
                    'reps': 12,
                    'weight': 40
                }
            ]
        })
        update_id = 1

        response = self.client().patch(
            f'/workouts/{update_id}',
            data=full_workout_string,
            content_type='application/json',
            headers=ATHLETE_HEADER
        )

        data = json.loads(response.data)

        with self.app.app_context():
            matching_workout = Workout.query.filter(Workout.name == 'updated workout').first()
            matching_exercises = len(matching_workout.exercises)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(matching_workout)
        self.assertEqual(matching_exercises, 1)

    def test_update_workout_out_of_bounds(self):
        full_workout_string = json.dumps({
            'name': 'updated workout',
            'focus': 'upper',
            'repeat': False,
            'exercises': [
                {
                    'name': 'kb goblet squat',
                    'sets': 4,
                    'reps': 12,
                    'weight': 40
                }
            ]
        })
        update_id = 11

        response = self.client().patch(
            f'/workouts/{update_id}',
            data=full_workout_string,
            content_type='application/json',
            headers=ATHLETE_HEADER
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_workout_bad_exercise(self):
        full_workout_string = json.dumps({
            'name': 'updated workout',
            'focus': 'upper',
            'repeat': False,
            'exercises': [
                {
                    'name': 'kb goblet squat',
                    'sets': 4,
                    'reps': 12,
                    'weight': 40
                },
                {
                    'name': 'not an exercise',
                    'sets': 100,
                    'reps': 6,
                    'weight': 0.5
                }
            ]
        })
        update_id = 1

        response = self.client().patch(
            f'/workouts/{update_id}',
            data=full_workout_string,
            content_type='application/json',
            headers=ATHLETE_HEADER
        )

        data = json.loads(response.data)

        with self.app.app_context():
            matching_workout = Workout.query.filter(Workout.name == 'updated workout')
            old_workout = Workout.query.filter(Workout.name == 'test workout')
            previous_mapping = WorkoutExercise.query.first()
            previous_mapping_weight = previous_mapping.weight

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNotNone(matching_workout)
        self.assertIsNotNone(old_workout)
        self.assertEqual(previous_mapping_weight, 4)

    def test_update_exercise(self):
        exercise_id = 1
        exercise_string = json.dumps({
            'name': 'barbell front squat',
            'equipment': 'barbell',
            'target': 'reps',
            'link': 'link to video here'
        })

        response = self.client().patch(
            f'/exercises/{exercise_id}',
            data=exercise_string,
            content_type='application/json',
            headers=COACH_HEADER
        )
        data = json.loads(response.data)

        with self.app.app_context():
            matching_exercises = Exercise.query.filter(Exercise.name == 'barbell front squat').count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(matching_exercises, 1)

    def test_update_exercise_out_of_bounds(self):
        exercise_id = 11
        exercise_string = json.dumps({
            'name': 'barbell front squat',
            'equipment': 'barbell',
            'target': 'reps',
            'link': 'link to video here'
        })

        response = self.client().patch(
            f'/exercises/{exercise_id}',
            data=exercise_string,
            content_type='application/json',
            headers=COACH_HEADER
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_no_header(self):
        response = self.client().get('/workouts')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_exercise_permission_error(self):
        exercise_string = json.dumps({
            'name': 'bodyweight squat',
            'equipment': 'bodyweight',
            'target': 'reps',
            'link': 'another link...'
        })
        response = self.client().post(
            '/exercises',
            data=exercise_string,
            content_type='application/json',
            headers=ATHLETE_HEADER
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_workout_permission_error(self):
        response = self.client().delete('/workouts/1', headers=ATHLETE_HEADER)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
