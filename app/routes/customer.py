from flask import Blueprint, request, jsonify
import re
from app.models.customer import Customer  # Import the Customer model
from app.db import db  # Import the db object for database interaction

# Create a Blueprint for customer-related routes
customer_bp = Blueprint('customers', __name__, url_prefix='/customers')


@customer_bp.route('/', methods=['POST'])
def create_customer():
    """
    Creates a new customer in the system.
    This function handles HTTP POST requests to create a new customer in the database.
    It validates the input data, ensures the userId is unique, and adds the customer to the database if all validations pass.
    Args:
        None: The function expects a JSON payload in the request body with the following fields:
            - userId (str): The email address of the customer (must be in a valid email format).
            - name (str): The name of the customer.
            - phone (str): The phone number of the customer.
            - address (str): The primary address of the customer.
            - address2 (str, optional): The secondary address of the customer (if any).
            - city (str): The city of the customer.
            - state (str): The 2-letter US state abbreviation of the customer.
            - zipcode (str): The ZIP code of the customer.
    Returns:
        Response: A JSON response with the created customer details and a 201 status code if successful.
        Response: A JSON response with an error message and a 400, 422, or 500 status code in case of validation errors,
                  duplicate userId, or unexpected errors respectively.
    """
    try:
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

        # Check if userId already exists in the database
        if Customer.query.filter_by(userId=data['userId']).first():
            return jsonify({"message": "This user ID already exists in the system."}), 422

        # Create a new customer object
        new_customer = Customer(
            userId=data['userId'],
            name=data['name'],
            phone=data['phone'],
            address=data['address'],
            address2=data.get('address2'),  # Optional field
            city=data['city'],
            state=data['state'],
            zipcode=data['zipcode']
        )

        # Add the new customer to the database
        db.session.add(new_customer)
        db.session.commit()

        # Return success response with the created customer data
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
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"message": "An error occurred while creating the customer", "error": str(e)}), 500


@customer_bp.route('/<id>', methods=['GET'])
def get_customer_by_id(id):
    """
    Retrieves customer details by their numeric ID.
    This function handles HTTP GET requests to fetch customer information from the database
    based on the provided customer ID. It validates the input, ensures the customer exists,
    and returns the customer's details if found.
    Args:
        id (str): The numeric ID of the customer to be retrieved, passed as a string.
    Returns:
        Response: A JSON response with the customer's details and a 200 status code if successful.
        Response: A JSON response with an error message and a 400 status code if the input is invalid.
        Response: A JSON response with an error message and a 404 status code if the customer is not found.
        Response: A JSON response with an error message and a 500 status code in case of unexpected errors.
    """
    try:
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
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"message": "An error occurred while retrieving the customer", "error": str(e)}), 500


@customer_bp.route('/', methods=['GET'])
def get_customer_by_user_id():
    """
    Retrieves customer details based on the provided user ID.
    This function handles HTTP GET requests to fetch customer information from the database
    using the user ID provided as a query parameter. It validates the user ID format and
    ensures the customer exists in the database.
    Args:
        None: The user ID is extracted from the query parameters of the HTTP request.
    Returns:
        Response: A JSON response containing the customer details and a 200 status code if successful.
        Response: A JSON response with an error message and a 400 status code if the user ID is missing
                  or has an invalid format.
        Response: A JSON response with an error message and a 404 status code if the user ID is not found.
        Response: A JSON response with an error message and a 500 status code in case of unexpected errors.
    
    """
    try:
        # Retrieve userId from query parameters
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({"message": "Missing userId query parameter"}), 400

        # Validate email format for userId using regex
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
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"message": "An error occurred while retrieving the customer", "error": str(e)}), 500