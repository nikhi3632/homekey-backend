from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class TestModel(db.Model):
    __tablename__ = 'test'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
    task_progress = db.Column(JSONB, default={})  # Task progress stored as JSON
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, name, email, password_hash=None):
        self.name = name
        self.email = email
        self.password_hash = password_hash

    # Method to hash the password before saving the user
    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Method to check if the password matches the hashed password
    def check_password_hash(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
