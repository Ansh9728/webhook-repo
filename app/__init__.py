from flask import Flask
from flask_pymongo import PyMongo
from app.api.routes import webhook
from app.config import Config

mongo_client = PyMongo()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    mongo_client.init_app(app)
    
    app.register_blueprint(webhook)

    return app
