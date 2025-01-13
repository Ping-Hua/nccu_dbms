import os
import requests
import logging
import re
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

class ISBNService:
    GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
    @staticmethod
    def fetch_book_by_isbn(isbn):
        try:
            # 驗證 API Key
            api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
            if not api_key:
                raise Exception("Google Books API key not found in environment variables.")

            # 設置請求參數
            params = {
                "q": f"isbn:{isbn}",
                "key": api_key
            }
            logging.info(f"Fetching book data for ISBN: {isbn} with params: {params}")

            response = requests.get(ISBNService.GOOGLE_BOOKS_API_URL, params=params)
            response.raise_for_status()

            data = response.json()
            print(f"Google Books API Response: {data}")

            if "items" not in data or not data["items"]:
                logging.warning(f"No books found for ISBN: {isbn}")
                return None

            book_info = data["items"][0].get("volumeInfo", {})
            book_picture_url = book_info.get("imageLinks", {}).get("thumbnail", "")

            book_data = {
                "ISBN": isbn,
                "book_name": book_info.get("title", "Unknown Title"),
                "author": ", ".join(book_info.get("authors", ["Unknown Author"])),
                "public_year": book_info.get("publishedDate", "Unknown").split("-")[0],
                "publisher": book_info.get("publisher", "Unknown"),
                "book_picture_url": book_picture_url
            }

            logging.info(f"Book data fetched successfully: {book_data}")
            return book_data

        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP request failed: {e}")
            return None
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return None