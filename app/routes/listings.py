from flask import Blueprint, request, jsonify
from app.models import db, User, Listing, Document 
from app.utils import login_required
from app.routes.documents import format_document
from sqlalchemy.orm.attributes import flag_modified

listings_bp = Blueprint('listings', __name__)

@listings_bp.route('/notify_fsh', methods=['POST'])
#@login_required
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
    flag_modified(user, 'task_progress')
    db.session.commit()

    return jsonify({'message': 'FSH notified of intent to sell successfully', 'document_id': new_document.id}), 201

@listings_bp.route('/prepare_home', methods=['POST'])
#@login_required
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
    flag_modified(user, 'task_progress')
    db.session.commit()

    return jsonify({'message': 'Home marked as photo-ready'}), 200

@listings_bp.route('/upload_photo', methods=['POST'])
#@login_required
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
    flag_modified(user, 'task_progress')
    db.session.commit()

    return jsonify({'message': 'Photo uploaded successfully', 'document_id': new_document.id}), 201

@listings_bp.route('/create_listing', methods=['POST'])
#@login_required
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
    flag_modified(user, 'task_progress')
    db.session.commit()

    return jsonify({'message': 'Listing created and entered into FSH system', 'listing_id': new_listing.id}), 201

@listings_bp.route('/get_all_listings', methods=['GET'])
##@login_required
def get_all_listings():
    """
    Fetch all listings for Buyers and FSH agents.
    - Buyers can only see listings with 'Approved' status.
    - FSH agents can see all listings.
    """
    user_id = request.args.get('user_id')
    # return  jsonify(user_id)
    # Fetch the user
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Ensure the user is either a Buyer or FSH agent
    if user.role.role_name not in ['Buyer', 'FSH']:
        return jsonify({'error': 'Only Buyers or FSH agents can view listings'}), 403

    # If the user is a Buyer, filter listings with 'Approved' status
    if user.role.role_name == 'Buyer':
        listings = Listing.query.filter_by(status='Approved').all()
    else:
        # If the user is FSH agent, fetch all listings (no filter by status)
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
            'created_at': listing.created_at,
            'documents': [format_document(doc) for doc in listing.documents],
            'bedrooms': listing.bedrooms,
            'bathrooms': listing.bathrooms,
            'squarefootage': listing.squarefootage
        }
        for listing in listings
    ]

    return jsonify(listings_data), 200

@listings_bp.route('/get_my_listings', methods=['GET'])
#@login_required
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
            'created_at': listing.created_at,
            'documents': [format_document(doc) for doc in listing.documents]
        }
        for listing in listings
    ]

    return jsonify(listings_data), 200

@listings_bp.route('/get_listing_by_id', methods=['GET'])
#@login_required
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
        'created_at': listing.created_at,
        'documents': [format_document(doc) for doc in listing.documents]
    }

    return jsonify(listing_data), 200

@listings_bp.route('/update_listing', methods=['PUT'])
#@login_required
def update_listing():
    """
    Allow the Seller to update their own listing (title, price, description, address) or just documents.
    """
    data = request.get_json()
    listing_id = data.get('listing_id')  # Listing to update
    user_id = data.get('user_id')  # Seller's user ID
    title = data.get('title')
    price = data.get('price')
    description = data.get('description')
    address = data.get('address')
    document_updates = data.get('documents')  # List of documents to update or add

    # Validate required fields: listing_id and user_id
    if not listing_id or not user_id:
        return jsonify({'error': 'listing_id and user_id are required'}), 400

    # Fetch the listing and the Seller
    listing = Listing.query.get(listing_id)
    user = User.query.get(user_id)

    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    if not user or user.role.role_name != 'Seller':
        return jsonify({'error': 'Invalid user or role'}), 403

    # Ensure the user is the owner of the listing
    if listing.seller_id != user.id:
        return jsonify({'error': 'You can only update your own listings'}), 403

    # Update the listing if fields are provided
    if title:
        listing.title = title
    if price:
        listing.price = price
    if description:
        listing.description = description
    if address:
        listing.address = address

    # Handle document updates (add, replace, or delete documents)
    if document_updates:
        for document in document_updates:
            # Handle document deletion
            if document.get('action') == 'delete':
                doc_id = document.get('document_id')
                document_to_delete = Document.query.get(doc_id)
                if document_to_delete:
                    db.session.delete(document_to_delete)
                else:
                    return jsonify({'error': f'Document with ID {doc_id} not found'}), 404
            
            # Handle document update or add
            elif document.get('action') in ['update', 'add']:
                # If it's an update or new document, handle file upload
                file = request.files.get(f"document_{document.get('document_id')}")
                if file:
                    file_name = file.filename
                    file_data = file.read()  # Read the file as binary

                    # If updating an existing document
                    if document.get('action') == 'update' and document.get('document_id'):
                        doc_id = document.get('document_id')
                        document_to_update = Document.query.get(doc_id)
                        if document_to_update:
                            document_to_update.file_name = file_name
                            document_to_update.file_data = file_data
                            db.session.commit()
                        else:
                            return jsonify({'error': f'Document with ID {doc_id} not found'}), 404
                    # If it's a new document
                    elif document.get('action') == 'add':
                        new_document = Document(
                            listing_id=listing.id,
                            uploaded_by=user.id,
                            document_type=document.get('document_type'),
                            file_name=file_name,
                            file_data=file_data
                        )
                        db.session.add(new_document)

        db.session.commit()

    return jsonify({'message': 'Listing and documents updated successfully', 'listing_id': listing.id}), 200


@listings_bp.route('/get_pending_listings', methods=['GET'])
#@login_required
def get_pending_listings():
    """
    Fetch all listings with 'Pending Approval' status for FSH agent review.
    """
    user_id = request.args.get('user_id')

    # Fetch the FSH agent
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Ensure the user is an FSH agent
    if user.role.role_name != 'FSH':
        return jsonify({'error': 'Only FSH agents can view pending listings'}), 403

    # Fetch all pending listings (no filtering by seller_id)
    pending_listings = Listing.query.filter_by(status='Pending Approval').all()

    # Prepare response data
    listings_data = [
        {
            'id': listing.id,
            'title': listing.title,
            'price': listing.price,
            'description': listing.description,
            'address': listing.address,
            'seller_id': listing.seller_id,
            'created_at': listing.created_at,
            'documents': [format_document(doc) for doc in listing.documents]
        }
        for listing in pending_listings
    ]

    return jsonify(listings_data), 200

@listings_bp.route('/approve_listing', methods=['POST'])
#@login_required
def approve_listing():
    """
    Approve a listing and update FSH agent's task progress.
    """
    data = request.get_json()
    user_id = data.get('user_id')  # FSH agent's user ID
    listing_id = data.get('listing_id')

    if not user_id or not listing_id:
        return jsonify({'error': 'user_id and listing_id are required'}), 400

    # Fetch FSH agent and listing
    fsh_agent = User.query.get(user_id)
    listing = Listing.query.get(listing_id)

    if not fsh_agent or not listing:
        return jsonify({'error': 'User or listing not found'}), 404

    # Ensure the user is an FSH agent
    if fsh_agent.role.role_name != 'FSH':
        return jsonify({'error': 'Only FSH agents can approve listings'}), 403

    # Ensure the listing is still pending approval
    if listing.status != 'Pending Approval':
        return jsonify({'error': 'Listing is not pending approval'}), 400

    # Approve the listing
    listing.status = 'Approved'

    # Update FSH agent's task progress
    task_progress = fsh_agent.task_progress.get('FSH', {})
    task_progress['approve_listing_in_fsh'] = True
    fsh_agent.task_progress['FSH'] = task_progress

    # Save changes to the database
    flag_modified(fsh_agent, 'task_progress')
    db.session.commit()

    return jsonify({'message': 'Listing approved successfully', 'listing_id': listing.id}), 200
