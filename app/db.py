from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy.pool import QueuePool

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with Flask app and enable connection pooling."""
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "poolclass": QueuePool,   # Use QueuePool for connection pooling
        "pool_size": 10,          # Maintain up to 10 persistent connections
        "max_overflow": 20,       # Allow 20 additional connections if needed
        "pool_timeout": 30,       # Wait up to 30 seconds for a connection
        "pool_recycle": 1800      # Recycle connections after 30 mins to prevent stale connections
    }
    
    db.init_app(app)

    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))  # Test the database connection
            print("Database connected successfully.")
        except SQLAlchemyError as e:
            print(f"Database connection error: {e}")

