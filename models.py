import os
from sqlalchemy import Column, String, Integer, Date, Time, create_engine
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


class Workout(db.Model):
    __tablename__ = 'Workouts'

    id = Column(Integer(), primary_key=True)
    date = Column(Date(), nullable=False)
    category = Column(String(), nullable=False)
    subcategory = Column(String())
    time = Column(Time(), nullable=False)

    def __init__(self, date, category, subcategory, time):
        self.date = date
        self.category = category
        self.subcategory = subcategory
        self.time = time

    def format(self):
        return {
            'id': self.id,
            'date': self.name,
            'category': self.category,
            'subcategory': self.subcategory,
            'time': self.time
        }
