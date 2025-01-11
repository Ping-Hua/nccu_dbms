from flask import jsonify, request
import logging
from app.services.genre_services import GenreService

class GenreController:
    def get_genres(self):
        logging.info("----Genre_controller.get_all_genres----")

        genre_list = GenreService.get_genres()
        return genre_list, 200

genre_controller = GenreController()