from flask import Flask
from dotenv import load_dotenv
import os

from app.webhook.routes import webhook
from app.extensions import mongo

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    mongo.init_app(app)

    app.register_blueprint(webhook)

    return app