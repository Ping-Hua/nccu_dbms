from flask import Blueprint
from app.controllers.book_controller import book_controller
from app.controllers.isbn_controller import isbn_controller

book_bp = Blueprint('book', __name__)

book_bp.add_url_rule('/add_book', view_func=book_controller.add_book, methods=['POST'])
book_bp.add_url_rule('/update_book', view_func=book_controller.update_book, methods=['PUT'])
book_bp.add_url_rule('/booklist', view_func=book_controller.get_booklist, methods=['GET'])
book_bp.add_url_rule('/booklist/<int:genre_id>', view_func=book_controller.get_booklist, methods=['GET'])
book_bp.add_url_rule('/search_books', view_func=book_controller.search_books, methods=['GET'])
book_bp.add_url_rule('/get_book_by_isbn', view_func=isbn_controller.get_book_by_isbn, methods=['GET'])
book_bp.add_url_rule('/book/details', view_func=book_controller.book_details, methods=['GET'])
