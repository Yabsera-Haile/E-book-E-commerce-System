# Import the create_app function from the app package's __init__.py file
from app.__init__ import create_app

# Create an instance of the Flask application using the factory function
app = create_app()

# Run the application if this script is executed directly
if __name__ == "__main__":
    # Start the Flask development server on host 0.0.0.0 and port 5000 with debug mode enabled
    app.run(host="0.0.0.0", port=4000, debug=True)
