import os
from flask import Flask, request
from app.routes.auth_routes import auth_bp
from app.routes.book_routes import book_bp
from app.routes.post_routes import post_bp
from app.routes.reply_routes import reply_bp
from app.routes.genre_routes import genre_bp
from app.routes.home_routes import home_bp
from . import database
from flask_cors import CORS

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # CORS(app , supports_credentials=True, origins=["http://localho.st:5173"])   
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://127.0.0.1:5173"}})

    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    
    # Session
    app.config['SECRET_KEY'] = os.urandom(24)

    # app.config['SESSION_COOKIE_NAME'] = 'Cookie-based_session'
    app.config['SESSION_COOKIE_NAME'] = 'session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True 
    app.config['SESSION_COOKIE_SECURE'] = False 
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800 # 1800 秒有效期

    app.config['DATABASE'] = 'database.db'
    database.init_app(app)
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(home_bp, url_prefix='/api/v1/')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(book_bp, url_prefix='/api/v1/book')
    app.register_blueprint(post_bp, url_prefix='/api/v1/post')
    app.register_blueprint(reply_bp, url_prefix='/api/v1/reply')
    app.register_blueprint(genre_bp, url_prefix='/api/v1/genre')
    
    return app