import os
from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.book_routes import book_bp
from app.routes.post_routes import post_bp
from app.routes.reply_routes import reply_bp
from app.routes.home_routes import home_bp
from app.errors import error_handler
from app import database
from flask_cors import CORS
from flask_session import Session

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    
    # Session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './flask_session'
    app.config['SESSION_PERMANENT'] = False # Session 不永久有效
    app.config['SESSION_USE_SIGNER'] = True # Session ID
    app.config['SECRET_KEY'] = os.urandom(24)
    Session(app)

    app.config['DATABASE'] = 'database.db'
    database.init_app(app)

    error_handler.register_error_handlers(app)
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    app.register_blueprint(home_bp, url_prefix='/api/v1/')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(book_bp, url_prefix='/api/v1/book')
    app.register_blueprint(post_bp, url_prefix='/api/v1/post')
    app.register_blueprint(reply_bp, url_prefix='/api/v1/reply')
    
    return app