from flask import Flask
from flask_pymongo import PyMongo
from app.api.routes import webhook
from app.config import Config
from flask_cors import CORS

mongo_client = PyMongo()

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder="../templates")
    CORS(app)

    app.config.from_object(Config)

    # mongo_client.init_app(app)
    mongo = PyMongo(app)
    app.extensions['pymongo'] = mongo
    
    app.register_blueprint(webhook)

    return app
