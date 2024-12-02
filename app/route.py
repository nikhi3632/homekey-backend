from flask import Blueprint, jsonify
from app import db
from app.models import TestModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return jsonify({"message": "Welcome to the Homekey Backend API"})

@main_bp.route('/test-db')
def test_db():
    try:
        # Create the tables
        db.create_all()
        
        # Create a test record
        test_record = TestModel(name="test_connection")
        db.session.add(test_record)
        db.session.commit()
        
        # Query the record
        result = TestModel.query.first()
        
        return jsonify({
            "status": "success",
            "message": "Database connection successful",
            "data": {
                "id": result.id,
                "name": result.name,
                "created_at": result.created_at.isoformat()
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }), 500
