import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Exercise, Workout, WorkoutExercise

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

            for value in [name, focus, repeat]:
                if value is None:
                    abort(400)

            workout = Workout(
                name=name,
                focus=focus,
                repeat=repeat
            )

            # could check whether we expect this to fail based on inputs, and abort(500) otherwise
            workout.insert()
        except:
            abort(400)

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

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # TODO revert back to 0.0.0.0 when not running locally
