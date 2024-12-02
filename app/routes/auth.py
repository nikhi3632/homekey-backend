from flask import Blueprint, request, jsonify, session
from app.models import db, User, Role, UserRoles
from utils import login_required

auth_bp = Blueprint('auth', __name__)

'''
During registration, a user will provide only one role (Buyer, Seller, or FSH).
The email must be unique for each user. If the same person wants to register with a different role, they must provide a different email.
A user can have multiple roles, but they will be differentiated by the email (i.e., each role requires a separate registration with a unique email).
A session will store only one role at a time, which will be active during the session.
'''

# Register route (with one role per user)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Extract data
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')  # Only one role here, e.g., "buyer", "seller", "fsh"

    if not name or not email or not password or not role_name:
        return jsonify({'error': 'Name, email, password, and role are required'}), 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400

    # Check if the role exists
    role = Role.query.filter_by(role_name=role_name).first()
    if not role:
        return jsonify({'error': f"Role '{role_name}' does not exist"}), 400

    # Create new user and hash the password
    new_user = User(name=name, email=email)
    new_user.hash_password(password)

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Assign the role to the user
    user_role = UserRoles(user_id=new_user.id, role_id=role.id)
    db.session.add(user_role)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    role_name = data.get('role')  # The role the user wants to log in with

    if not email or not password or not role_name:
        return jsonify({'error': 'Email, password, and role are required'}), 400

    # Fetch user by email
    user = User.query.filter_by(email=email).first()
    if user and user.check_password_hash(password):
        # Check if the user has the requested role
        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            return jsonify({'error': f'Role {role_name} does not exist'}), 400

        # Ensure the user has the requested role
        user_role = UserRoles.query.filter_by(user_id=user.id, role_id=role.id).first()
        if not user_role:
            return jsonify({'error': f'User does not have the {role_name} role'}), 400

        # Store user ID and role in the session
        session['user_id'] = user.id
        session['role'] = role_name

        return jsonify({'message': 'Login successful', 'user_id': user.id, 'role': role_name}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Logout Route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/protected_route', methods=['GET'])
@login_required
def protected_route():
    # This route is only accessible if the user is logged in
    return jsonify({'message': 'This is a protected route.'})
