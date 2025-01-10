from app.database import use_db
import logging
from app.errors.custom_exceptions import ResourceNotFoundError, ValidationError

class AuthService:
    @staticmethod
    @use_db
    def register_user(cursor, username, email, password, student_number, phone):

        if not all([username, email, password, student_number, phone]):
            raise ValidationError("All fields are required: username, email, password, student_number, phone")

        cursor.execute("SELECT COUNT(*) FROM user WHERE email = ?", (email,))
        if cursor.fetchone()[0] > 0:
            raise ValidationError(f"Email {email} is already registered")

        # # 檢查 Student Number
        # cursor.execute("SELECT COUNT(*) FROM user WHERE student_number = ?", (student_number,))
        # if cursor.fetchone()[0] > 0:
        #     raise ValidationError(f"Student number {student_number} is already registered")

        # # 檢查 Phone 是否已存在
        # cursor.execute("SELECT COUNT(*) FROM user WHERE phone = ?", (phone,))
        # if cursor.fetchone()[0] > 0:
        #     raise ValidationError(f"Phone {phone} is already registered")


        cursor.execute(
            "INSERT INTO user (username, email, password, student_number, phone) VALUES (?, ?, ?, ?, ?)",
            (username, email, password, student_number, phone)
        )
        logging.info("User registered successfully")
        return cursor.lastrowid

    @staticmethod
    @use_db
    def get_user_by_email(cursor, email):
        if not email:
            raise ValidationError("Email is required")

        cursor.execute(
            "SELECT user_id, username, email, password FROM user WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        if not user:
            raise ResourceNotFoundError(f"User with email {email} not found")
        return {
            "user_id": user[0],
            "username": user[1],
            "email": user[2],
            "password": user[3]
        }
