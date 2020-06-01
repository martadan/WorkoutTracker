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
        return jsonify(formatted_exercises)

    @app.route('/workouts')
    def get_workouts():
        workouts = Workout.query.all()
        formatted_workouts = [w.format() for w in workouts]
        return jsonify(formatted_workouts)

    @app.route('/mappings')
    def get_mappings():
        mappings = WorkoutExercise.query.all()
        formatted_mappings = [m.format() for m in mappings]
        return jsonify(formatted_mappings)

    @app.route('/test/create_exercises')
    def test_create_exercises():
        ex1 = Exercise(
            name='kb swing',
            equipment='kettlebell',
            target='reps',
            link='dummy link'
        )
        ex2 = Exercise(
            name='kb goblet squat',
            equipment='kettlebell',
            target='reps',
            link='another dummy link here'
        )
        ex1.insert()
        ex2.insert()

        return jsonify({
            'success': True
        })

    @app.route('/test/create_workout')
    def test_create_workout():
        w = Workout(
            name='test workout',
            focus='legs',
            repeat=False
        )
        w.insert()

        w_returned = Workout.query.filter(Workout.name == 'test workout').first()

        return jsonify({
            'success': True,
            'id': w_returned.id
        })

    @app.route('/test/create_mapping')
    def test_create_mapping():
        w = Workout.query.first()
        e = Exercise.query.first()

        m = WorkoutExercise(
            workout_id=w.id,
            exercise_id=e.id,
            sets=3,
            reps=8,
            weight=4
        )

        m.insert()

        return jsonify({
            'success': True
        })

    @app.route('/test/delete_exercises')
    def test_delete_exercises():
        exercises = Exercise.query.all()
        for e in exercises:
            e.delete()
        return jsonify({
            'success': True
        })

    @app.route('/test/delete_workouts')
    def test_delete_workouts():
        workouts = Workout.query.all()
        for w in workouts:
            w.delete()
        return jsonify({
            'success': True
        })

    @app.route('/test/delete_mapping')
    def test_delete_mapping():
        maps = WorkoutExercise.query.all()
        for m in maps:
            m.delete()
        return jsonify({
            'success': True
        })

    @app.route('/test/delete_all')
    def delete_all():
        test_delete_mapping()
        test_delete_exercises()
        test_delete_workouts()
        return jsonify({'success': True})

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
