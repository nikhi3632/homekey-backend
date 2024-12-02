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

class Listing(db.Model):
    __tablename__ = 'listings'
    
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for the listing
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))  # Foreign key to the Users table
    title = db.Column(db.String(255), nullable=False)  # Title of the listing
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price of the property
    description = db.Column(db.Text)  # Description of the property
    address = db.Column(db.Text)  # Address of the property
    status = db.Column(db.String(50), default='Pending Approval')  # Status of the listing
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))  # Timestamp when the listing was created
    
    seller = db.relationship('User', backref='listings', lazy=True)  # Relationship to User (Seller)
    documents = db.relationship('Document', backref='listing', lazy=True)  # Relationship to Documents

    def __init__(self, seller_id, title, price, description, address, status='Pending Approval'):
        self.seller_id = seller_id
        self.title = title
        self.price = price
        self.description = description
        self.address = address
        self.status = status

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for the document
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id', ondelete='CASCADE'))  # Foreign key to Listings table
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))  # Foreign key to Users table
    document_type = db.Column(db.String(50), nullable=False)  # Type of document (e.g., Notification, Photo)
    file_name = db.Column(db.String(255), nullable=False)  # Original file name
    file_data = db.Column(db.LargeBinary, nullable=False)  # Binary data of the file
    uploaded_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))  # Timestamp for when the document was uploaded
    
    listing = db.relationship('Listing', backref='documents', lazy=True)  # Relationship to Listing
    uploader = db.relationship('User', backref='uploaded_documents', lazy=True)  # Relationship to User (Uploader)

    def __init__(self, listing_id, uploaded_by, document_type, file_name, file_data):
        self.listing_id = listing_id
        self.uploaded_by = uploaded_by
        self.document_type = document_type
        self.file_name = file_name
        self.file_data = file_data
