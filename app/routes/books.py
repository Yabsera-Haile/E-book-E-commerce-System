from flask import Blueprint, request, jsonify
from app.models.book import Book  # Import the Book model
from app.db import db  # Import the db object for database interaction

# Create a Blueprint for books-related routes
books_bp = Blueprint('books', __name__, url_prefix='/books')

# Route to get all books (just for testing)
@books_bp.route('/isbn/<isbn>', methods=['GET'])
@books_bp.route('/<isbn>', methods=['GET'])
def get_book(isbn):
    book = Book.query.filter_by(ISBN=isbn).first()
    if not book:
        return jsonify({"message": "ISBN not found"}), 404

    response_body = {
        "ISBN": book.ISBN,
        "title": book.title,
        "Author": book.author,
        "description": book.description,
        "genre": book.genre,
        "price": book.price,
        "quantity": book.quantity
    }
    return jsonify(response_body), 200

# Route to add a new book
@books_bp.route('/', methods=['POST'])
def add_book():
    # Get data from the request body
    data = request.get_json()
    try:
        # Validate all mandatory fields are present
        required_fields = ['ISBN', 'title', 'Author', 'description', 'genre', 'price', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"message": f"{field} is a mandatory field and cannot be empty."}), 400

        # Check if ISBN already exists
        if Book.query.filter_by(ISBN=data['ISBN']).first():
            return jsonify({"message": "This ISBN already exists in the system."}), 422

        # Check if price has exactly two decimal points
        if not isinstance(data['price'], (float, str)) or not (len(str(data['price']).split('.')[-1]) == 2):
            return jsonify({"message": "Price must have exactly two decimal points."}), 400
        # Create a new Book instance
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

        response_body = {
            "ISBN": new_book.ISBN,
            "title": new_book.title,
            "Author": new_book.author,
            "description": new_book.description,
            "genre": new_book.genre,
            "price": new_book.price,
            "quantity": new_book.quantity
        }
        response = jsonify(response_body)
        response.status_code = 201
        response.headers['Location'] = f"{request.host_url}books/{new_book.ISBN}"
        return response

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred.{e}"}), 500


@books_bp.route('/<isbn>', methods=['PUT'])
def update_book(isbn):
    book = Book.query.filter_by(ISBN=isbn).first()
    if not book:
        return jsonify({"message": "ISBN not found"}), 404

    # Get data from the request body
    data = request.get_json()
    try:
        # Validate all mandatory fields are present
        required_fields = ['title', 'Author', 'description', 'genre', 'price', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"message": f"{field} is a mandatory field and cannot be empty."}), 400

        # Check if price has exactly two decimal points
        if not isinstance(data['price'], (float, str)) or not (len(str(data['price']).split('.')[-1]) == 2):
            return jsonify({"message": "Price must have exactly two decimal points."}), 400

        # Update the book details
        book.title = data['title']
        book.author = data['Author']
        book.description = data['description']
        book.genre = data['genre']
        book.price = float(data['price'])
        book.quantity = int(data['quantity'])

        # Commit the changes to the database
        db.session.commit()

        response_body = {
            "ISBN": book.ISBN,
            "title": book.title,
            "Author": book.author,
            "description": book.description,
            "genre": book.genre,
            "price": book.price,
            "quantity": book.quantity
        }
        return jsonify(response_body), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred.{e}"}), 500
    