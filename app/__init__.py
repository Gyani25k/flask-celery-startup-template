from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy

# Flask App and SQLAlchemy Initialization
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # SQLite Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Celery Configuration
    app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'db+sqlite:///database.db'

    db.init_app(app)

    return app

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery
