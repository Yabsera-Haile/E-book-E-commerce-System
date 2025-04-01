from app.db import db
from sqlalchemy.orm import validates

# Define the Book model (table)
class Book(db.Model):
    __tablename__ = 'books'  # Name of the table in the database
    
    # Define the columns of the table
    ISBN = db.Column(db.String(200), primary_key=True, nullable=False, unique=True)  # Primary key, unique identifier for each book
    title = db.Column(db.String(200), nullable=False)  # Title of the book
    author = db.Column(db.String(200), nullable=False)  # Author of the book
    description = db.Column(db.Text, nullable=False)  # Description or summary of the book
    genre = db.Column(db.String(200), nullable=False)  # Genre or category of the book
    price = db.Column(db.Float, nullable=False)  # Price of the book
    quantity = db.Column(db.Integer, nullable=False)  # Quantity of the book available in stock
    
    # Constructor to initialize a Book object
    def __init__(self, ISBN, title, author, description, genre, price, quantity):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.description = description
        self.genre = genre
        self.price = price
        self.quantity = quantity

    # String representation of the Book object for debugging and logging
    def __repr__(self):
        return f"<Book {self.title} (ISBN: {self.ISBN})>"
