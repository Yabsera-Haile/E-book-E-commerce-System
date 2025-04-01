from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy.pool import QueuePool

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask app and configure connection pooling.

    Args:
        app: The Flask application instance.
    """
    # Configure SQLAlchemy connection pooling options
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "poolclass": QueuePool,   # Use QueuePool for efficient connection pooling
        "pool_size": 10,          # Maintain up to 10 persistent connections in the pool
        "max_overflow": 20,       # Allow up to 20 additional connections beyond the pool size
        "pool_timeout": 30,       # Wait up to 30 seconds for a connection to become available
        "pool_recycle": 1800      # Recycle connections after 30 minutes to prevent stale connections
    }
    
    # Bind the SQLAlchemy object to the Flask app
    db.init_app(app)

    # Test the database connection within the app context
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))  # Execute a simple query to test the connection
            print("Database connected successfully.")
        except SQLAlchemyError as e:
            # Log an error message if the connection test fails
            print(f"Database connection error: {e}")
