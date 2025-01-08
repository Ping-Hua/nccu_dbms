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

        if not all([isbn, book_name, author, version, public_year, publisher]):
            return jsonify({"error": "Missing required fields: ISBN, book_name, author, version, public_year, publisher"}), 400
        
        try:
            book = BookService.adding_book(isbn, book_name, author, version, public_year, publisher)
            return jsonify({
                'book_id': book['book_id'],
                'ISBN': book['ISBN'],
                'book_name': book['book_name'],
                'author': book['author'],
                'version': book['version'],
                'public_year': book['public_year'],
                'publisher': book['publisher']
            }), 201
        
        except ValueError as e:  
            logging.warning(str(e))
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            logging.error(f"Error adding book: {str(e)}")
            return jsonify({"success": False, "error": str(e)}),500
    
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
        user_query = request.args.get("query")  # 假設從查詢參數中獲取查詢query
        if  user_query is None or len(user_query) == 0:
            logging.warning("Book name is missing in the request.")
            return jsonify({"success": False, "error": "Book name is required"}), 400

        try:
            book_service = BookService()
            searching = book_service.search(user_query)
            if searching is not None and len(searching) > 0:
                logging.info(f"Books with query '{user_query}' retrieved successfully.")
                return jsonify({"success": True, "message": "Books searched successfully", "book": searching}), 200
                 
            else:
                logging.warning(f"Attempted to search non-existent book with  {user_query}")
                return jsonify({"success": False, "error": "Books not found"}),404
        except Exception as e:
            logging.error(f"Error occurred while searching book with {user_query}: {str(e)}")
            return jsonify({"success": False, "error": str(e)}),500
    
book_controller = BookController()