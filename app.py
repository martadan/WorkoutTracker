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

    @app.route('/exercises')
    def get_exercises():
        exercises = Exercise.query.all()
        formatted_exercises = [e.format() for e in exercises]
        return jsonify({
            'exercises': formatted_exercises,
            'success': True
        })

    @app.route('/workouts')
    def get_workouts():
        workouts = Workout.query.all()
        formatted_workouts = [w.format() for w in workouts]
        return jsonify({
            'workouts': formatted_workouts,
            'success': True
        })

    @app.route('/mappings')
    def get_mappings():
        mappings = WorkoutExercise.query.all()
        formatted_mappings = [m.format() for m in mappings]
        return jsonify(formatted_mappings)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # TODO revert back to 0.0.0.0 when not running locally
