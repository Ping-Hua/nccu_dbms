from flask import jsonify, request
import logging
from app.services.book_service import BookService

class BookController:
    def add_book(self):
        logging.info("----Book_controller.add_book----")

        data = request.get_json()

        isbn = data.get('ISBN')
        book_name = data.get('book_name')
        author = data.get('author') 
        version = data.get('version')
        public_year = data.get('public_year')
        publisher = data.get('publisher')
        book_picture_url = data.get('book_picture_url')

        book = BookService.adding_book(isbn, book_name, author, version, public_year, publisher, book_picture_url)
        return jsonify({
            'book_id': book['book_id'],
            'ISBN': book['ISBN'],
            'book_name': book['book_name'],
            'author': book['author'],
            'version': book['version'],
            'public_year': book['public_year'],
            'publisher': book['publisher'],
            'book_picture_url' : book['book_picture_url']
        }), 201
        
    def update_book(self):
        logging.info("----Book_controller.update_book----")

        # TODO: 實現修改書籍邏輯
        return jsonify({"message": "Book updated successfully"})
    
    def get_books(self):
        logging.info("----Book_controller.get_books----")

        # TODO: 實現獲得書籍資料邏輯
        return jsonify({"message": "Books retrieved successfully", "books": []})
    
    def list_books(self):
        logging.info("----Book_controller.list_books----")

        # TODO: 實現獲得書籍列表邏輯
        return jsonify({"message": "Books listed successfully", "books": []})
    
    def search_books(self):
        logging.info("----Book_controller.search_books----")

        # TODO: 實現書籍搜尋邏輯
        return jsonify({"message": "Books searched successfully", "books": []})
    
book_controller = BookController()