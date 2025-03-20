from app.db import db
from sqlalchemy.orm import validates

# Define the Book model (table)
class Book(db.Model):
    __tablename__ = 'books'
    
    ISBN = db.Column(db.String(200), primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    def __init__(self, ISBN, title, author, description, genre, price, quantity):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.description = description
        self.genre = genre
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"<Book {self.title} (ISBN: {self.ISBN})>"
