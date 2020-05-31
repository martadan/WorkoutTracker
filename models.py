import os
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Date, Time, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


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

class Workout(db.Model):
    __tablename__ = 'Workouts'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(), nullable=False, unique=True),
    focus = Column(String(), nullable=True),
    repeat = Column(Boolean(), nullable=False),
    created = Column(DateTime(), nullable=False)

    def __init__(self, name, focus, repeat, created):
        self.name = name
        self.focus = focus
        self.repeat = repeat
        self.created = created

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'focus': self.focus,
            'repeat': self.repeat,
            'created': self.created
        }


class Exercise(db.Model):
    __tablename__ = 'Exercises'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(), nullable=False, unique=True)
    equipment = Column(String(), nullable=False)
    target = Column(String(), nullable=False)  # reps or time
    link = Column(String(), nullable=True)  # link to exercise video/explanation
    # double_weight = Column(Boolean(), nullable=False)  # double the weight in total volume calculation (using two dbs)
    # add_bodyweight = Column(Boolean(), nullable=False)  # add bodyweight to total volume calcluation

    def __init__(self, name, equipment, target, link):
        self.name = name
        self.equipement = equipment
        self.target = target
        self.link = link

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'equipment': self.equipment,
            'target': self.target,
            'link': self.link
        }
