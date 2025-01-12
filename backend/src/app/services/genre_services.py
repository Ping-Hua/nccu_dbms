from app.database import use_db
from app.errors.custom_exceptions import ResourceNotFoundError

class GenreService:
    @staticmethod
    @use_db
    def get_genres(cursor):
        cursor.execute(
            "SELECT genre_id, genre_name FROM genre"
        )
        genres = cursor.fetchall()
        if genres is None:
            raise ResourceNotFoundError("Unable to find book list")
        genres_json = []
        for genre in genres:
            genre_data = {
                "genre_id": genre[0],
                "genre_name": genre[1],
            }
            genres_json.append(genre_data)
        return genres_json