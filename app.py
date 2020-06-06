import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Exercise, Workout, WorkoutExercise
from auth import CustomAuthError, requires_auth

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """
    Create and configure the app
    """
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/', methods=['GET'])
    def home_page():
        return render_template('home.html')

    @app.route('/workouts', methods=['GET'])
    def get_workouts():
        workouts = Workout.query.all()
        formatted_workouts = [w.format() for w in workouts]
        return jsonify({
            'workouts': formatted_workouts,
            'success': True
        })

    @app.route('/workouts', methods=['POST'])
    def create_workout():
        try:
            all_data = request.get_json()
            name = all_data['name']
            focus = all_data['focus']
            repeat = all_data['repeat']
            if 'exercises' in all_data.keys():
                exercises = all_data['exercises']
            else:
                exercises = None

            for value in [name, focus, repeat]:
                if value is None:
                    abort(400)

            workout = Workout(
                name=name,
                focus=focus,
                repeat=repeat
            )
        except:
            abort(400)

        if exercises is None:
            # insert Workout with no WorkoutExercises rows
            try:
                workout.insert()
            except:
                abort(400)
        else:
            # insert Workout, get id, then create WorkoutExercises rows
            try:
                workout.insert_without_commit()
                for exercise in exercises:
                    e_id = Exercise.query.filter(Exercise.name == exercise['name']).first().id
                    workout_exercise = WorkoutExercise(
                        workout_id=workout.id,
                        exercise_id=e_id,
                        sets=exercise['sets'],
                        reps=exercise['reps'],
                        weight=exercise['weight']
                    )
                    workout_exercise.insert_without_commit()
                workout.update()
            except:
                abort(404)

        return jsonify({
            'success': True,
            'id': workout.id
        })

    @app.route('/workouts/<int:workout_id>', methods=['GET'])
    def get_workout(workout_id):
        workout = Workout.query.get(workout_id)
        if workout is not None:
            return jsonify({
                'success': True,
                'workout': workout.format()
            })
        else:
            abort(404)

    @app.route('/workouts/<int:workout_id>', methods=['DELETE'])
    def delete_workout(workout_id):
        workout = Workout.query.get(workout_id)

        if workout is None:
            abort(404)
        else:
            try:
                workout.delete()
            except:
                abort(404)

            return jsonify({
                'success': True,
                'workout_id': workout_id
            })

    @app.route('/workouts/<int:workout_id>', methods=['PATCH'])
    def update_workout(workout_id):
        workout = Workout.query.get(workout_id)
        if workout is None:
            abort(404)

        try:
            all_data = request.get_json()
            name = all_data['name']
            focus = all_data['focus']
            repeat = all_data['repeat']
            if 'exercises' in all_data.keys():
                exercises = all_data['exercises']
            else:
                exercises = None
            for value in [name, focus, repeat]:
                if value is None:
                    abort(400)

            workout.name = name
            workout.focus = focus
            workout.repeat = repeat

            for current_exercise in workout.exercises:
                current_exercise.delete_without_commit()
        except:
            abort(400)

        try:
            for exercise in exercises:
                e_id = Exercise.query.filter(Exercise.name == exercise['name']).first().id
                workout_exercise = WorkoutExercise(
                    workout_id=workout.id,
                    exercise_id=e_id,
                    sets=exercise['sets'],
                    reps=exercise['reps'],
                    weight=exercise['weight']
                )
                workout_exercise.insert_without_commit()

            workout.update()
        except:
            abort(404)

        return jsonify({
            'success': True,
            'id': workout.id
        })

    @app.route('/exercises', methods=['GET'])
    def get_exercises():
        exercises = Exercise.query.all()
        formatted_exercises = [e.format() for e in exercises]
        return jsonify({
            'exercises': formatted_exercises,
            'success': True
        })

    @app.route('/exercises', methods=['POST'])
    def create_exercise():
        try:
            all_data = request.get_json()
            name = all_data['name']
            equipment = all_data['equipment']
            target = all_data['target']
            link = all_data['link']

            for value in [name, equipment, target, link]:
                if value is None:
                    abort(400)

            exercise = Exercise(
                name=name,
                equipment=equipment,
                target=target,
                link=link
            )

            # could check whether we expect this to fail based on inputs, and abort(500) otherwise
            exercise.insert()
        except:
            abort(400)

        return jsonify({
            'success': True,
            'id': exercise.id
        })

    @app.route('/exercises/<int:exercise_id>', methods=['GET'])
    def get_exercise(exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if exercise is not None:
            return jsonify({
                'success': True,
                'exercise': exercise.format()
            })
        else:
            abort(404)

    @app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
    def delete_exercise(exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if exercise is None:
            abort(404)
        elif WorkoutExercise.query.filter(WorkoutExercise.exercise_id == exercise_id).count() > 0:
            abort(400)
        else:
            try:
                exercise.delete()
            except:
                abort(500)

            return jsonify({
                'success': True,
                'exercise_id': exercise_id
            })

    @app.route('/exercises/<int:exercise_id>', methods=['PATCH'])
    def update_exercise(exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if exercise is None:
            abort(404)

        try:
            all_data = request.get_json()
            name = all_data['name']
            equipment = all_data['equipment']
            target = all_data['target']
            link = all_data['link']

            exercise.name = name
            exercise.equipment = equipment
            exercise.target = target
            exercise.link = link

            exercise.update()
        except:
            abort(400)

        return jsonify({
            'success': True,
            'exercise_id': exercise_id
        })

    # probably actually don't need this one - can't think of why I'd need to query the mappings themselves
    @app.route('/mappings', methods=['GET'])
    def get_mappings():
        mappings = WorkoutExercise.query.all()
        formatted_mappings = [m.format() for m in mappings]
        return jsonify(formatted_mappings)

    # error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'server error'
        }), 500

    @app.errorhandler(CustomAuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # TODO revert back to 0.0.0.0 when not running locally
