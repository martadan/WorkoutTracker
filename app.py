import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


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

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
