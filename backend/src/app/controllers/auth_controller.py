from flask import jsonify, request, session
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.auth_service import AuthService

class AuthController:
    def register(self):
        logging.info("----Auth_controller.register----")

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        student_number = data.get('student_number')
        phone = data.get('phone')

        if not all([username, email, password, student_number, phone]):
            return jsonify({"message": "Missing required fields"}), 400

        try:
            hashed_password = generate_password_hash(password)

            user_id = AuthService.register_user(
                username = username,
                email = email,
                password = hashed_password,
                student_number = student_number,
                phone = phone
            )

            return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
        except Exception as e:
            logging.exception("Error during registration")
            return jsonify({"message": f"Error: {str(e)}"}), 500

    def login(self):
        logging.info("----Auth_controller.login----")

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({"message": "Missing email or password"}), 400

        try:
            user = AuthService.get_user_by_email(email)

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                return jsonify({"message": "User logged in successfully"}), 200
            else:
                return jsonify({"message": "Invalid email or password"}), 401
        except Exception as e:
            logging.exception("Error during login")
            return jsonify({"message": f"Error: {str(e)}"}), 500

    def logout(self):
        logging.info("----Auth_controller.logout----")

        try:
            session.clear()
            return jsonify({"message": "User logged out successfully"}), 200
        except Exception as e:
            logging.exception("Error during logout")
            return jsonify({"message": f"Error: {str(e)}"}), 500

auth_controller = AuthController()
