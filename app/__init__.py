from flask import Flask
from db import init_db
import os

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    init_db(app)

    @app.route("/status")
    def home():
        return {"message": "OK"}

    return app