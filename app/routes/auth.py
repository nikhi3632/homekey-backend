from flask import Blueprint, request, jsonify, session
from app.models import db, User, Role
from app.utils import login_required
from sqlalchemy import exc

auth_bp = Blueprint('auth', __name__)

'''
During registration, a user will provide only one role (Buyer, Seller, or FSH).
The email must be unique for each user. If the same person wants to register with a different role, they must provide a different email.
A user can have only one role at a time, and this role will be stored in the session.
'''

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')

    # Validate input data
    if not name or not email or not password or not role_name:
        return jsonify({'error': 'Name, email, password, and role are required'}), 400

    # Check if email already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400

    # Fetch the role from the database
    role = Role.query.filter_by(role_name=role_name).first()
    if not role:
        return jsonify({'error': f"Role '{role_name}' not found"}), 400

    # Create a new User instance and hash the password
    new_user = User(name=name, email=email)
    new_user.hash_password(password)
    new_user.role = role  # Assign the single role to the user

    # Initialize task progress based on the assigned role
    new_user.task_progress = new_user.initialize_task_progress(role)

    # Add the new user to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id, 'role': role_name}), 201
    except exc.SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'error': str(e)}), 500

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Fetch user by email
    user = User.query.filter_by(email=email).first()

    # If user does not exist or password doesn't match
    if not user or not user.check_password_hash(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Get the user's role
    user_role = user.role.role_name

    # Retrieve the user's task progress for their role
    task_progress = user.task_progress.get(user_role, {})

    # Store role in the session
    session['user_id'] = user.id
    session['role'] = user_role

    # Return the user data (e.g., user ID, role, and task progress)
    return jsonify({
        'user_id': user.id,
        'role': user_role,
        'task_progress': task_progress
    }), 200

# Logout Route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)     # Remove role from session
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/protected_route', methods=['GET'])
#@login_required
def protected_route():
    # This route is only accessible if the user is logged in
    return jsonify({'message': 'This is a protected route.'})
