import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from models import Exercise, Workout, WorkoutExercise


def create_app(test_config=None):
    """
    Create and configure the app
    :param test_config:
    :return:
    """
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def home_page():
        return render_template('home.html')

    # @app.route('/exercises')
    # def get_exercises():
    #     exercises = Exercise.query.all()
    #     formatted_exercises = [e.format() for e in exercises]
    #     return jsonify(formatted_exercises)

    # @app.route('/test/create_exercise')
    # def test_create_exercise():
    #     ex1 = Exercise(
    #         name='kb swing',
    #         equipment='kettlebell',
    #         target='reps',
    #         link='dummy link'
    #     )
    #     ex2 = Exercise(
    #         name='kb goblet squat',
    #         equipment='kettlebell',
    #         target='reps',
    #         link='another dummy link here'
    #     )
    #     ex1.insert()
    #     ex2.insert()
    #
    #     return jsonify({
    #         'success': True
    #     })

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
