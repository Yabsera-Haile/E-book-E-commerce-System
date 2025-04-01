from flask import Flask
from app.db import init_db
import os
from app.routes import blueprints  # Import all routes

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Database connection string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy event system to save resources

    # Initialize the database with the Flask app
    init_db(app)

    # Register all blueprints (modularized routes) with the Flask app
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # Define a simple status route to check if the app is running
    @app.route("/status")
    def home():
        return {"message": "OK"}  # Return a JSON response indicating the app is running

    return app  # Return the configured Flask app instance