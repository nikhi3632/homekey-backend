from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS
from flask_session import Session

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow all origins for simplicity, adjust as necessary for production
    app.config.from_object(Config)
    # Initialize SQLAlchemy before Flask-Session
    db.init_app(app)
    # Now set up Flask-Session with SQLAlchemy as the session interface
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db  # Provide the existing db instance to Flask-Session    
    # Initialize Flask-Session
    Session(app)
    from app.route import main_bp
    app.register_blueprint(main_bp)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.routes.documents import document_bp
    app.register_blueprint(document_bp, url_prefix='/documents')
    from app.routes.escrow import escrow_bp
    app.register_blueprint(escrow_bp, url_prefix='/escrow')
    from app.routes.listings import listings_bp
    app.register_blueprint(listings_bp, url_prefix='/listings')
    from app.routes.offers import offers_bp
    app.register_blueprint(offers_bp, url_prefix='/offers')
    from app.routes.task_progress import task_progress_bp
    app.register_blueprint(task_progress_bp, url_prefix='/task_progress')
    
    # Import models to ensure they are registered with SQLAlchemy
    from app import models
    return app