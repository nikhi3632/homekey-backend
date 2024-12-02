from flask import Blueprint, request, jsonify
from models import db, User
from sqlalchemy.exc import SQLAlchemyError
from tasks import TASK_SEQUENCES  # Import task sequences for role-based tasks

bp = Blueprint('task_progress', __name__)

@bp.route('/complete_task', methods=['POST'])
def complete_task():
    data = request.get_json()
    user_id = data.get('user_id')  # User ID
    task_name = data.get('task_name')  # Task name to be marked as completed

    # Ensure the user ID and task_name are provided
    if not user_id or not task_name:
        return jsonify({'error': 'user_id and task_name are required'}), 400

    # Fetch the user by ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get the user's role
    user_role = user.role.role_name

    # Check if the task exists for the user's role
    if user_role not in TASK_SEQUENCES or task_name not in TASK_SEQUENCES[user_role]:
        return jsonify({'error': f"Task '{task_name}' not found for role '{user_role}'"}), 400

    # Initialize task progress for the role if not already set
    if user_role not in user.task_progress:
        user.task_progress[user_role] = {task: False for task in TASK_SEQUENCES[user_role]}

    # Mark the task as completed (set the task progress to True)
    user.task_progress[user_role][task_name] = True

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Task completed successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'error': str(e)}), 500

@bp.route('/get_task_progress', methods=['GET'])
def get_task_progress():
    user_id = request.args.get('user_id')  # Get user_id from the query parameter

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    # Fetch the user by ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get the user's role
    user_role = user.role.role_name

    # Fetch task progress for the user's role
    task_progress = user.task_progress.get(user_role, {})

    # Return the user's task progress for their role
    return jsonify({
        'user_id': user.id,
        'role': user_role,
        'task_progress': task_progress
    }), 200
