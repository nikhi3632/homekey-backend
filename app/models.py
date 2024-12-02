from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from flask_bcrypt import Bcrypt
from routes.tasks import TASK_SEQUENCES

db = SQLAlchemy()
bcrypt = Bcrypt()

class TestModel(db.Model):
    __tablename__ = 'test'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)  # Role name (e.g., Seller, Buyer, FSH)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)  # Email must be unique
    password_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
    task_progress = db.Column(JSONB, default={})  # Task progress stored as JSON
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # Foreign key to Roles table
    role = db.relationship('Role', backref='users', lazy=True)  # Relationship to Role

    def __init__(self, name, email, password_hash=None, role=None):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role  # only one role is assigned
        self.task_progress = self.initialize_task_progress(role)

    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password_hash(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def initialize_task_progress(self, role):
        task_progress = {}
        if role and role.role_name in TASK_SEQUENCES:
            task_progress[role.role_name] = {task: False for task in TASK_SEQUENCES[role.role_name]}
        return task_progress

