from flask import jsonify, request
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
        ## TODO: 實現登入邏輯
         
        return jsonify({"message": "User logged in successfully"})
    
    def logout(self):
        logging.info("----Auth_controller.logout----")
        ## TODO: 實現登出邏輯
         
        return jsonify({"message": "User logged out successfully"})
    

auth_controller = AuthController()