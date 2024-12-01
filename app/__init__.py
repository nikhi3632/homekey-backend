from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow all origins for simplicity, adjust as necessary for production
    app.config.from_object(Config)
    db.init_app(app)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Import models to ensure they are registered with SQLAlchemy
    from app import models

    return app
