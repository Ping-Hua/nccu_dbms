from flask import jsonify
from app.errors.custom_exceptions import ResourceNotFoundError, DatabaseError, ValidationError

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({'error': 'Validation error occured', 'messages': str(e)}), 400

    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_not_found_error(e):
        return jsonify({'error': 'Resource Not Found error occured', 'messages': str(e)}), 404

    @app.errorhandler(DatabaseError)
    def handle_database_error(e):
        return jsonify({'error': 'Database error occured', 'messages': str(e)}), 500
    
    @app.errorhandler(Exception)
    def handle_general_error(e):
        return jsonify({'error': 'An unexpected error occurred', 'messages': str(e)}), 500

    