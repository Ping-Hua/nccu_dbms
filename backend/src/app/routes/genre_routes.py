from flask import Blueprint
from app.controllers.genre_controller import genre_controller

genre_bp = Blueprint('genre', __name__)

genre_bp.add_url_rule('/genres', view_func=genre_controller.get_genres, methods=['GET'])
