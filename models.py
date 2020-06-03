import os
import json
import datetime as dt
from sqlalchemy import Column, ForeignKey, String, Integer, Numeric, DateTime, Boolean, Date, Time, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = 'Workouts'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(), nullable=False, unique=True)
    focus = Column(String(), nullable=True)
    repeat = Column(Boolean(), nullable=False)
    created = Column(DateTime(), nullable=False)
    exercises = relationship('WorkoutExercise', backref='workouts')

    def __init__(self, name, focus, repeat):
        self.name = name
        self.focus = focus
        self.repeat = repeat
        self.created = dt.datetime.now()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'focus': self.focus,
            'repeat': self.repeat,
            'created': self.created,
            'exercises': [e.format() for e in self.exercises]
        }

    def format_short(self):
        return json.dumps({
            'name': self.name,
            'focus': self.focus,
            'repeat': self.repeat
        })

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def insert_without_commit(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


class Exercise(db.Model):
    __tablename__ = 'Exercises'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(), nullable=False, unique=True)
    equipment = Column(String(), nullable=False)
    target = Column(String(), nullable=False)  # reps or time
    link = Column(String(), nullable=True)  # link to exercise video/explanation
    # double_weight = Column(Boolean(), nullable=False)  # double the weight in total volume calculation (using two dbs)
    # add_bodyweight = Column(Boolean(), nullable=False)  # add bodyweight to total volume calculation

    def __init__(self, name, equipment, target, link):
        self.name = name
        self.equipment = equipment
        self.target = target
        self.link = link

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'equipment': self.equipment,
            'target': self.target,
            'link': self.link,
            'in_workouts': [m.workouts.name for m in self.workout_exercises]
        }

    def format_short(self):
        return json.dumps({
            'name': self.name,
            'equipment': self.equipment,
            'target': self.target,
            'link': self.link
        })

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


class WorkoutExercise(db.Model):
    __tablename__ = 'WorkoutExercises'

    id = Column(Integer(), primary_key=True, nullable=False)
    workout_id = Column(Integer(), ForeignKey('Workouts.id'))
    exercise_id = Column(Integer(), ForeignKey('Exercises.id'))
    sets = Column(Integer(), nullable=False)
    reps = Column(Integer(), nullable=False)
    weight = Column(Numeric(precision=3, scale=1), nullable=False)
    exercise = relationship('Exercise', backref='workout_exercises')

    def __init__(self, workout_id, exercise_id, sets, reps, weight):
        self.workout_id = workout_id
        self.exercise_id = exercise_id
        self.sets = sets
        self.reps = reps
        self.weight = weight

    def format(self):
        return {
            'id': self.id,
            'workout_id': self.workout_id,
            'exercise_id': self.exercise_id,
            'name': self.exercise.name,
            'equipment': self.exercise.equipment,
            'link': self.exercise.link,
            'sets': self.sets,
            'reps': self.reps,
            'weight': str(self.weight)  # Decimal() is not json serializable apparently...
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


# Will possibly expand to this in the future, but not yet
# class Event(db.Model):
#     __tablename__ = 'Events'
#
#     id = Column(Integer(), primary_key=True)
#     date = Column(Date(), nullable=False)
#     category = Column(String(), nullable=False)
#     subcategory = Column(String())
#     time = Column(Time(), nullable=False)
#
#     def __init__(self, date, category, subcategory, time):
#         self.date = date
#         self.category = category
#         self.subcategory = subcategory
#         self.time = time
#
#     def format(self):
#         return {
#             'id': self.id,
#             'date': self.name,
#             'category': self.category,
#             'subcategory': self.subcategory,
#             'time': self.time
#         }


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def drop_db(app):
    db.drop_all()
