from flask import jsonify, request, session
import logging
from app.services.auth_service import AuthService

class AuthController:
    def register(self):
        logging.info("----Auth_controller.register----")
        
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        student_number = data.get('student_number')
        phone = data.get('phone')
        user_name = data.get('user_name') 

        register = AuthService.register(email, password, student_number, phone, user_name)
        return jsonify({
            'user_id': register['user_id'],
            'student_number': register['student_number'],
            'email': register['email'],
            'phone': register['phone'],
            'user_name': register['user_name'],
        }), 201
    
    def login(self):
        session.clear()
        logging.info("----Auth_controller.login----")
        
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        login = AuthService.login(email, password)

        session['user_id'] = login['user_id']
        session['email'] = login['email']
        session.permanent = True
        # print("------------")
        # print(session)
        # print("------------")

        return jsonify({
            'message': 'Login successful' ,
            'user': {
            'user_id': login['user_id'],
            'email': login['email'],
            }
        }), 200
    
    def logout(self):
        logging.info("----Auth_controller.logout----")
        # print("Request Cookies:", request.cookies)
        # print("Session content:", session)
        
        if 'user_id' in session:
            user_id = session.get('user_id')
            logging.info(f"User {user_id} logged out")

            session.clear()
            logging.info("Session cleared successfully")
         
            return jsonify({
                "message": "Logout successfully"}), 200
        else:
            logging.warning("Logout attempt without a valid session")
            return jsonify({
                "error": "No active session found",
                "message": "You are not logged in"
            }), 400
    
    def check_status(self):
        logging.info("----Auth_controller.check_status----")
        # print("Request Cookies:", request.cookies)
        # print("Session content:", session)
        if 'user_id' in session:
            user_id = session.get('user_id')
            email = session.get('email')
            logging.info(f"User {user_id} is logged in")

            return jsonify({
                'logged_in': True,
                'user': {
                    'user_id': user_id,
                    'email': email
                }
            }), 200
        else:
            logging.info("No active session found")
            return jsonify({
                'logged_in': False,
                'message': "No user is logged in"
            }), 200

auth_controller = AuthController()