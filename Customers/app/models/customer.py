from app.db import db
from sqlalchemy.orm import validates

# Define the Customer model (table)
class Customer(db.Model):
    __tablename__ = 'customers'  # Name of the table in the database

    # Define the columns for the customers table
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key, auto-incremented
    userId = db.Column(db.String(255), nullable=False, unique=True)  # Unique user identifier
    name = db.Column(db.String(255), nullable=False)  # Customer's name
    phone = db.Column(db.String(255), nullable=False)  # Customer's phone number
    address = db.Column(db.String(255), nullable=False)  # Primary address
    address2 = db.Column(db.String(255), nullable=True)  # Secondary address (optional)
    city = db.Column(db.String(255), nullable=False)  # City of residence
    state = db.Column(db.String(255), nullable=False)  # State of residence
    zipcode = db.Column(db.String(255), nullable=False)  # Zip code

    # Constructor to initialize a Customer object
    def __init__(self, userId, name, phone, address, city, state, zipcode, address2=None):
        self.userId = userId  # Assign userId
        self.name = name  # Assign name
        self.phone = phone  # Assign phone
        self.address = address  # Assign primary address
        self.address2 = address2  # Assign secondary address (if provided)
        self.city = city  # Assign city
        self.state = state  # Assign state
        self.zipcode = zipcode  # Assign zip code