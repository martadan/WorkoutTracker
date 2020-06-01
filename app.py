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

    @app.route('/')
    def home_page():
        return render_template('home.html')

    @app.route('/exercises', methods=['GET'])
    def get_exercises():
        exercises = Exercise.query.all()
        formatted_exercises = [e.format() for e in exercises]
        return jsonify({
            'exercises': formatted_exercises,
            'success': True
        })

    @app.route('/workouts', methods=['GET'])
    def get_workouts():
        workouts = Workout.query.all()
        formatted_workouts = [w.format() for w in workouts]
        return jsonify({
            'workouts': formatted_workouts,
            'success': True
        })

    # probably actually don't need this one - can't think of why I'd need to query the mappings themselves
    @app.route('/mappings', methods=['GET'])
    def get_mappings():
        mappings = WorkoutExercise.query.all()
        formatted_mappings = [m.format() for m in mappings]
        return jsonify(formatted_mappings)

    @app.route('/exercises/<int:exercise_id>', methods=['GET'])
    def get_exercise(exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if exercise is not None:
            return jsonify({
                'success': True,
                'exercise': exercise.format()
            })
        else:
            return jsonify({
                'success': False
            }), 404

    @app.route('/workouts/<int:workout_id>', methods=['GET'])
    def get_workout(workout_id):
        workout = Workout.query.get(workout_id)
        if workout is not None:
            return jsonify({
                'success': True,
                'workout': workout.format()
            })
        else:
            return jsonify({
                'success': False
            }), 404

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # TODO revert back to 0.0.0.0 when not running locally
