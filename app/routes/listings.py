from flask import Blueprint, request, jsonify
from app.models import db, User, Listing, Document 
from utils import login_required
from sqlalchemy import exc

bp = Blueprint('listing', __name__)

@bp.route('/notify_fsh', methods=['POST'])
@login_required
def notify_fsh():
    """
    Upload a notification document for the Seller notifying FSH of intent to sell.
    """
    file = request.files.get('document')
    user_id = request.form.get('user_id')  # Seller's ID

    if not (file and user_id):
        return jsonify({'error': 'Document and user_id are required'}), 400

    # Fetch the Seller user
    user = User.query.get(user_id)
    if not user or user.role.role_name != 'Seller':
        return jsonify({'error': 'Invalid user or role'}), 403

    # Upload document to the Documents table
    file_name = file.filename
    file_data = file.read()  # Read the file as binary

    new_document = Document(
        listing_id=None,  # No listing yet; this is a notification
        uploaded_by=user.id,
        document_type='Notification',
        file_name=file_name,
        file_data=file_data
    )
    db.session.add(new_document)
    db.session.commit()

    # Update task progress for the Seller
    task_progress = user.task_progress.get('Seller', {})
    task_progress['notify_fsh_intent_to_sell'] = True
    user.task_progress['Seller'] = task_progress
    db.session.commit()

    return jsonify({'message': 'FSH notified of intent to sell successfully', 'document_id': new_document.id}), 201

@bp.route('/prepare_home', methods=['POST'])
@login_required
def prepare_home():
    """
    Mark the home as photo-ready for the listing.
    """
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    # Fetch the Seller
    user = User.query.get(user_id)
    if not user or user.role.role_name != 'Seller':
        return jsonify({'error': 'Invalid user or role'}), 403

    # Ensure the previous task (notify_fsh_intent_to_sell) is completed
    task_progress = user.task_progress.get('Seller', {})
    if not task_progress.get('notify_fsh_intent_to_sell', False):
        return jsonify({'error': 'You must notify FSH before preparing the home'}), 400

    # Mark the property as photo-ready
    task_progress['prepare_home_for_listing'] = True
    user.task_progress['Seller'] = task_progress
    db.session.commit()

    return jsonify({'message': 'Home marked as photo-ready'}), 200

@bp.route('/upload_photo', methods=['POST'])
@login_required
def upload_photo():
    """
    Upload a single photo for the listing.
    """
    file = request.files.get('photo')
    user_id = request.form.get('user_id')

    if not (file and user_id):
        return jsonify({'error': 'Photo and user_id are required'}), 400

    # Fetch the Seller
    user = User.query.get(user_id)
    if not user or user.role.role_name != 'Seller':
        return jsonify({'error': 'Invalid user or role'}), 403

    # Ensure the previous task (prepare_home_for_listing) is completed
    task_progress = user.task_progress.get('Seller', {})
    if not task_progress.get('prepare_home_for_listing', False):
        return jsonify({'error': 'You must prepare the home before uploading a photo'}), 400

    # Upload the photo as binary data
    file_name = file.filename
    file_data = file.read()

    # Save the photo as a Document linked to the Listing (later)
    new_document = Document(
        listing_id=None,  # No listing yet
        uploaded_by=user.id,
        document_type='Photo',
        file_name=file_name,
        file_data=file_data
    )
    db.session.add(new_document)
    db.session.commit()

    # Update task progress
    task_progress['provide_photo_for_listing'] = True
    user.task_progress['Seller'] = task_progress
    db.session.commit()

    return jsonify({'message': 'Photo uploaded successfully', 'document_id': new_document.id}), 201

@bp.route('/create_listing', methods=['POST'])
@login_required
def create_listing():
    """
    Finalize the listing and enter it into the FSH website.
    """
    user_id = request.json.get('user_id')
    title = request.json.get('title')
    price = request.json.get('price')
    description = request.json.get('description')
    address = request.json.get('address')

    if not (user_id and title and price and description and address):
        return jsonify({'error': 'All fields are required'}), 400

    # Fetch the Seller
    user = User.query.get(user_id)
    if not user or user.role.role_name != 'Seller':
        return jsonify({'error': 'Invalid user or role'}), 403

    # Ensure the previous task (photo upload) is completed
    task_progress = user.task_progress.get('Seller', {})
    if not task_progress.get('provide_photo_for_listing', False):
        return jsonify({'error': 'You must upload a photo before creating the listing'}), 400

    # Create the listing
    new_listing = Listing(
        seller_id=user.id,
        title=title,
        price=price,
        description=description,
        address=address,
        status='Pending Approval'
    )
    db.session.add(new_listing)
    db.session.commit()

    # Update task progress
    task_progress['enter_sale_listing_in_fsh'] = True
    user.task_progress['Seller'] = task_progress
    db.session.commit()

    return jsonify({'message': 'Listing created and entered into FSH system', 'listing_id': new_listing.id}), 201

@bp.route('/get_all_listings', methods=['GET'])
@login_required
def get_all_listings():
    """
    Fetch all listings for Buyers and FSH agents.
    """
    user_id = request.args.get('user_id')

    # Fetch the user
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Ensure the user is either a Buyer or FSH agent
    if user.role.role_name not in ['Buyer', 'FSH']:
        return jsonify({'error': 'Only Buyers or FSH agents can view all listings'}), 403

    # Fetch all listings (no filtering by seller_id)
    listings = Listing.query.all()

    # Prepare response data
    listings_data = [
        {
            'id': listing.id,
            'title': listing.title,
            'price': listing.price,
            'description': listing.description,
            'address': listing.address,
            'status': listing.status,
            'created_at': listing.created_at
        }
        for listing in listings
    ]

    return jsonify(listings_data), 200

@bp.route('/get_my_listings', methods=['GET'])
@login_required
def get_my_listings():
    """
    Fetch listings for the Seller. Only shows listings posted by that Seller.
    """
    user_id = request.args.get('user_id')

    # Fetch the user (Seller)
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Ensure the user is a Seller
    if user.role.role_name != 'Seller':
        return jsonify({'error': 'Only Sellers can view their own listings'}), 403

    # Fetch listings where the seller_id matches the user's ID
    listings = Listing.query.filter_by(seller_id=user_id).all()

    # Prepare response data
    listings_data = [
        {
            'id': listing.id,
            'title': listing.title,
            'price': listing.price,
            'description': listing.description,
            'address': listing.address,
            'status': listing.status,
            'created_at': listing.created_at
        }
        for listing in listings
    ]

    return jsonify(listings_data), 200

@bp.route('/get_listing_by_id', methods=['GET'])
@login_required
def get_listing_by_id():
    """
    Fetch details of a specific listing by listing_id.
    """
    listing_id = request.args.get('listing_id')

    if not listing_id:
        return jsonify({'error': 'listing_id is required'}), 400

    # Fetch the listing by ID
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    # Prepare response data
    listing_data = {
        'id': listing.id,
        'title': listing.title,
        'price': listing.price,
        'description': listing.description,
        'address': listing.address,
        'status': listing.status,
        'created_at': listing.created_at
    }

    return jsonify(listing_data), 200
