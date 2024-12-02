import os, db

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@db:5432/homekey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  # Enable debug mode
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY = db  # This refers to the SQLAlchemy instance
