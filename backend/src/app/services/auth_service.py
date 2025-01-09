from app.database import use_db
import logging
import bcrypt
from app.errors.custom_exceptions import ResourceNotFoundError, ValidationError

class AuthService:
    @staticmethod
    @use_db
    def register(cursor, email, password, student_number, phone, user_name):
        logging.info(f"Register user called with email={email}, student_number={student_number}, phone={phone}, username={user_name}")

        if any(v is None for v in [email, password, student_number, phone, user_name]):
            raise ValidationError("Missing required fields: email, password, student_number, phone, user_name")
        
        # Email 唯一
        cursor.execute("SELECT COUNT(*) FROM user WHERE email = ?", (email,))
        if cursor.fetchone()[0] > 0:
            raise ValidationError(f"Email: {email} already exists in the database.")

        # 學號唯一
        #cursor.execute("SELECT COUNT(*) FROM user WHERE student_number = ?", (student_number,))
        #if cursor.fetchone()[0] > 0:
        #    raise ValidationError(f"Student number: {student_number} already exists in the database.")
        
        logging.info(f"Registering user with password={password}") # 開發用
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO user (email, password, student_number, phone, user_name) VALUES (?,?,?,?,?)", 
            (email, hashed_password, student_number, phone, user_name)
        )

        user_id = cursor.lastrowid
        logging.info(f"User registered successfully: {user_id}")

        return {
            "user_id": user_id,
            "email": email,
            "student_number": student_number,
            "phone": phone,
            "user_name": user_name,
        }
