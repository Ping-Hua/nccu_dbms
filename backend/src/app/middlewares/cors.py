from flask import request

def cors_middleware(app):
    @app.before_request
    def handle_options_request():
        if request.method == "OPTIONS":
            response = app.response_class()
            response.headers["Access-Control-Allow-Origin"] = "http://localho.st:5173"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response
