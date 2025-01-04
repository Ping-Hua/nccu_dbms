from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'error': 'Resource not found', 'details': str(e)}), 404

    @app.errorhandler(400)
    def handle_400_error(e):
        return jsonify({'error': 'Bad Request', 'details': str(e)}), 400

    @app.errorhandler(500)
    def handle_500_error(e):
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    @app.errorhandler(Exception)
    def handle_general_error(e):
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
