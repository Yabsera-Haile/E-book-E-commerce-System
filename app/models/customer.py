from app.db import db
from sqlalchemy.orm import validates

# Define the Customer model (table)
class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    address2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zipcode = db.Column(db.String(255), nullable=False)
    
    def __init__(self, userId, name, phone, address, city, state, zipcode, address2=None):
        self.userId = userId
        self.name = name
        self.phone = phone
        self.address = address
        self.address2 = address2
        self.city = city
        self.state = state
        self.zipcode = zipcode