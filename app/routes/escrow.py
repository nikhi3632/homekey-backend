import base64
from flask import Blueprint, request, jsonify
from app.models import db, User, Listing, Escrow
from app.utils import login_required

escrow_bp = Blueprint('escrow', __name__)

@escrow_bp.route('/open_escrow', methods=['POST'])
#@login_required
def open_escrow():
    """
    FSH agent opens escrow for a listing and provides the escrow number.
    """
    data = request.get_json()
    user_id = data.get('user_id')  # FSH agent's ID
    listing_id = data.get('listing_id')  # Listing ID
    escrow_number = data.get('escrow_number')  # Escrow number

    # Validate inputs
    if not (user_id and listing_id and escrow_number):
        return jsonify({'error': 'user_id, listing_id, and escrow_number are required'}), 400

    # Fetch the FSH agent and listing
    user = User.query.get(user_id)
    listing = Listing.query.get(listing_id)

    if not user or user.role.role_name != 'FSH':
        return jsonify({'error': 'Only FSH agents can open escrow'}), 403

    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    # Ensure escrow doesn't already exist for this listing
    existing_escrow = Escrow.query.filter_by(listing_id=listing_id).first()
    if existing_escrow:
        return jsonify({'error': 'Escrow has already been opened for this listing'}), 400

    # Create a new escrow entry
    new_escrow = Escrow(
        listing_id=listing.id,
        seller_id=listing.seller_id,
        escrow_number=escrow_number,
        status="Open"  # Set initial status to "Open"
    )
    db.session.add(new_escrow)
    db.session.commit()

    # Update task progress for the FSH
    task_progress = user.task_progress.get('FSH', {})
    task_progress['open_escrow'] = True
    user.task_progress['FSH'] = task_progress

    # Save changes to the database
    db.session.commit()

    # Return success response
    return jsonify({'message': 'Escrow opened successfully', 'escrow_id': new_escrow.id}), 201
