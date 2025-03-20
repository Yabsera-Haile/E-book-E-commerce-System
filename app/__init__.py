from flask import Flask
from app.db import init_db
import os
from app.routes import blueprints  # Import all routes

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    init_db(app)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.route("/status")
    def home():
        return {"message": "OK"}

    return app