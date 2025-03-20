from flask import Blueprint, request, jsonify
import re
from app.models.customer import Customer  # Import the Book model
from app.db import db  # Import the db object for database interaction

# Create a Blueprint for books-related routes
customer_bp = Blueprint('customers', __name__, url_prefix='/customers')


@customer_bp.route('/',methods=['POST'])
def create_customer():
    data = request.get_json()

    # Validate required fields
    required_fields = ['userId', 'name', 'phone', 'address', 'city', 'state', 'zipcode']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"Missing or invalid field: {field}"}), 400

    # Validate email format for userId using regex
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, data['userId']):
        return jsonify({"message": "Invalid email format for userId"}), 400

    # Validate state as a 2-letter US state abbreviation
    valid_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 
        'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 
        'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    }
    if data['state'].upper() not in valid_states:
        return jsonify({"message": "Invalid state format. Must be a 2-letter US state abbreviation"}), 400

    # Check if userId already exists
    if Customer.query.filter_by(userId=data['userId']).first():
        return jsonify({"message": "This user ID already exists in the system."}), 422

    # Create a new customer
    new_customer = Customer(
        userId=data['userId'],
        name=data['name'],
        phone=data['phone'],
        address=data['address'],
        address2=data.get('address2'),
        city=data['city'],
        state=data['state'],
        zipcode=data['zipcode']
    )

    # Add to the database
    db.session.add(new_customer)
    db.session.commit()

    # Return success response
    response = {
        "id": new_customer.customer_id,
        "userId": new_customer.userId,
        "name": new_customer.name,
        "phone": new_customer.phone,
        "address": new_customer.address,
        "address2": new_customer.address2,
        "city": new_customer.city,
        "state": new_customer.state,
        "zipcode": new_customer.zipcode
    }
    return jsonify(response), 201, {'Location': f"/customers/{new_customer.customer_id}"}

@customer_bp.route('/<id>', methods=['GET'])
def get_customer_by_id(id):
    # Validate that id is numerical
    if not id.isdigit():
        return jsonify({"message": "Illegal, missing, or malformed input"}), 400

    # Retrieve customer by numeric ID
    customer = Customer.query.get(int(id))
    if not customer:
        return jsonify({"message": "Customer ID not found"}), 404

    # Return customer data
    response = {
        "id": customer.customer_id,
        "userId": customer.userId,
        "name": customer.name,
        "phone": customer.phone,
        "address": customer.address,
        "address2": customer.address2,
        "city": customer.city,
        "state": customer.state,
        "zipcode": customer.zipcode
    }
    return jsonify(response), 200


@customer_bp.route('/', methods=['GET'])
def get_customer_by_user_id():
    # Retrieve userId from query parameters
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"message": "Missing userId query parameter"}), 400
    
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, user_id):
        return jsonify({"message": "Invalid email format for userId"}), 400

    # Retrieve customer by userId
    customer = Customer.query.filter_by(userId=user_id).first()
    if not customer:
        return jsonify({"message": "User ID not found"}), 404

    # Return customer data
    response = {
        "id": customer.customer_id,
        "userId": customer.userId,
        "name": customer.name,
        "phone": customer.phone,
        "address": customer.address,
        "address2": customer.address2,
        "city": customer.city,
        "state": customer.state,
        "zipcode": customer.zipcode
    }
    return jsonify(response), 200