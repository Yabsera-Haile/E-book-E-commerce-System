from flask import Blueprint, request, jsonify
from app.models.book import Book  # Import the Book model
from app.db import db  # Import the db object for database interaction

# Create a Blueprint for books-related routes
books_bp = Blueprint('books', __name__, url_prefix='/books')


# Route to retrieve a book by its ISBN
@books_bp.route('/isbn/<isbn>', methods=['GET'])
@books_bp.route('/<isbn>', methods=['GET'])
def get_book(isbn):
    """
    Retrieves the details of a book identified by its ISBN.
    This function handles HTTP GET requests to fetch the details of a book from the database.
    It queries the database for the book with the given ISBN and returns its details if found.
    Args:
        isbn (str): The ISBN of the book to be retrieved.
    Returns:
        Response: A JSON response with the book details and a 200 status code if the book is found.
        Response: A JSON response with an error message and a 404 status code if the book is not found.
        Response: A JSON response with an error message and a 400 status code in case of a value error.
        Response: A JSON response with an error message and a 500 status code in case of unexpected errors.
    """
    
    try:
        # Query the database for a book with the given ISBN
        book = Book.query.filter_by(ISBN=isbn).first()
        if not book:
            # Return a 404 error if the book is not found
            return jsonify({"message": "ISBN not found"}), 404

        # Prepare the response body with book details
        response_body = {
            "ISBN": book.ISBN,
            "title": book.title,
            "Author": book.author,
            "description": book.description,
            "genre": book.genre,
            "price": book.price,
            "quantity": book.quantity
        }
        # Return the book details with a 200 status code
        return jsonify(response_body), 200

    except ValueError as e:
        # Handle value errors and return a 400 error
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        # Handle unexpected errors and return a 500 error
        return jsonify({"message": f"An unexpected error occurred. {e}"}), 500


# Route to add a new book
@books_bp.route('/', methods=['POST'])
def add_book():
    """
    Adds a new book to the system.
    This function handles HTTP POST requests to create a new book entry in the database.
    It validates the input data, checks for duplicate ISBNs, and ensures the price format is correct.
    If all validations pass, the book is added to the database.
    Returns:
        Response: A JSON response with the new book's details and a 201 status code if successful.
        Response: A JSON response with an error message and a 400, 422, or 500 status code in case of validation errors,
                  duplicate ISBN, or unexpected errors respectively.
    """

    # Get data from the request body
    data = request.get_json()
    try:
        # Validate that all mandatory fields are present
        required_fields = ['ISBN', 'title', 'Author', 'description', 'genre', 'price', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                # Return a 400 error if any mandatory field is missing or empty
                return jsonify({"message": f"{field} is a mandatory field and cannot be empty."}), 400

        # Check if a book with the same ISBN already exists
        if Book.query.filter_by(ISBN=data['ISBN']).first():
            # Return a 422 error if the ISBN already exists
            return jsonify({"message": "This ISBN already exists in the system."}), 422

        # Validate that the price has exactly two decimal points
        if not isinstance(data['price'], (float, str)) or not (len(str(data['price']).split('.')[-1]) == 2):
            # Return a 400 error if the price format is invalid
            return jsonify({"message": "Price must have exactly two decimal points."}), 400

        # Create a new Book instance with the provided data
        new_book = Book(
            ISBN=data['ISBN'],
            title=data['title'],
            author=data['Author'],
            description=data['description'],
            genre=data['genre'],
            price=float(data['price']),
            quantity=int(data['quantity'])
        )

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        # Prepare the response body with the new book's details
        response_body = {
            "ISBN": new_book.ISBN,
            "title": new_book.title,
            "Author": new_book.author,
            "description": new_book.description,
            "genre": new_book.genre,
            "price": new_book.price,
            "quantity": new_book.quantity
        }
        # Return the response with a 201 status code and a Location header
        response = jsonify(response_body)
        response.status_code = 201
        response.headers['Location'] = f"{request.host_url}books/{new_book.ISBN}"
        return response

    except ValueError as e:
        # Handle value errors and return a 400 error
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        # Handle unexpected errors and return a 500 error
        return jsonify({"message": f"An unexpected error occurred.{e}"}), 500


# Route to update an existing book by its ISBN
@books_bp.route('/<isbn>', methods=['PUT'])
def update_book(isbn):
    """
    Updates the details of a book identified by its ISBN.
    This function handles HTTP PUT requests to update the details of a book in the database.
    It validates the input data, ensures the ISBN in the request matches the book's ISBN,
    and updates the book's information if all validations pass.
    Args:
        isbn (str): The ISBN of the book to be updated, extracted from the URL.
    Returns:
        Response: A JSON response with the updated book details and a 200 status code if successful.
        Response: A JSON response with an error message and a 400, 404, or 500 status code in case of validation errors,
                book not found, or unexpected errors respectively.
    """
    # Get data from the request body
    data = request.get_json()
    try:
        # Validate that all mandatory fields are present
        required_fields = ['title', 'Author', 'description', 'genre', 'price', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                # Return a 400 error if any mandatory field is missing or empty
                return jsonify({"message": f"{field} is a mandatory field and cannot be empty."}), 400
        
        # Check if the ISBN in the request body matches the book's ISBN
        if 'ISBN' in data and data['ISBN'] != isbn:
            # Return a 400 error if the ISBN in the request body does not match the book's ISBN
            return jsonify({"message": "ISBN in the request body does not match the book's ISBN."}), 400

        # Validate that the price has exactly two decimal points
        if not isinstance(data['price'], (float, str)) or not (len(str(data['price']).split('.')[-1]) == 2):
            # Return a 400 error if the price format is invalid
            return jsonify({"message": "Price must have exactly two decimal points."}), 400
        
        # Query the database for a book with the given ISBN
        book = Book.query.filter_by(ISBN=isbn).first()
        if not book:
            # Return a 404 error if the book is not found
            return jsonify({"message": "ISBN not found"}), 404

        # Update the book details with the provided data
        book.title = data['title']
        book.author = data['Author']
        book.description = data['description']
        book.genre = data['genre']
        book.price = float(data['price'])
        book.quantity = int(data['quantity'])

        # Commit the changes to the database
        db.session.commit()

        # Prepare the response body with the updated book details
        response_body = {
            "ISBN": book.ISBN,
            "title": book.title,
            "Author": book.author,
            "description": book.description,
            "genre": book.genre,
            "price": book.price,
            "quantity": book.quantity
        }
        # Return the updated book details with a 200 status code
        return jsonify(response_body), 200

    except ValueError as e:
        # Handle value errors and return a 400 error
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        # Handle unexpected errors and return a 500 error
        return jsonify({"message": f"An unexpected error occurred.{e}"}), 500