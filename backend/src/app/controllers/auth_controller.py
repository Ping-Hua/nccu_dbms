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
        logging.info("----Auth_controller.login----")
        
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        login = AuthService.login(email, password)

        session['user_id'] = login['user_id']
        session['email'] = login['email']
        session.permanent = True

        return jsonify({
            'message': 'Login successful' ,
            'user': {
            'user_id': login['user_id'],
            'email': login['email'],
            }
        }), 200
    
    def logout(self):
        logging.info("----Auth_controller.logout----")
        
        session.clear()
        logging.info("User logged out, session cleared")
         
        return jsonify({
            "message": "Logout successfully"}), 200
    

auth_controller = AuthController()