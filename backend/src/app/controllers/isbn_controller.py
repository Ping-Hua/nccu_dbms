from flask import jsonify, request
import logging
from app.services.isbn_service import ISBNService


class ISBNController:
    def get_book_by_isbn(self):

        logging.info("----ISBNController.get_book_by_isbn----")
        isbn = request.args.get("isbn")

        if not isbn:
            logging.warning("ISBN is missing in the request")
            return jsonify({"success": False, "error": "ISBN is required"}), 400
        
        try:
            book_data = ISBNService.fetch_book_by_isbn(isbn)

            if not book_data:
                logging.warning(f"No book found for the given ISBN: {isbn}")
                return jsonify({"success": False, "message": "No book found for the given ISBN."}), 404

            logging.info(f"Book data found: {book_data}")
            return jsonify({"success": True, "book_data": book_data}), 200

        except Exception as e:
            logging.error(f"Error in ISBNController.get_book_by_isbn: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
        
isbn_controller = ISBNController()