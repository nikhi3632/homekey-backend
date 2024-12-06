from flask import Blueprint, request, jsonify
from app.models import db, User, Listing, Offer
from app.utils import login_required

# Create a Blueprint for offers
offers_bp = Blueprint('offers', __name__)

@offers_bp.route('/get_offers_for_listing', methods=['GET'])
# @login_required
def get_offers_for_listing():
    """
    Fetch all offers for a seller's listing.
    """
    user_id = request.args.get('user_id')  # Seller's user ID
    listing_id = request.args.get('listing_id')  # Listing ID to fetch offers for

    # Fetch the seller
    seller = User.query.get(user_id)
    if not seller or seller.role.role_name != 'Seller':
        return jsonify({'error': 'Invalid user or role'}), 403

    # Fetch the listing
    listing = Listing.query.get(listing_id)
    if not listing or listing.seller_id != seller.id:
        return jsonify({'error': 'Listing not found or you are not the seller of this listing'}), 404

    # Fetch all offers for the listing
    offers = Offer.query.filter_by(listing_id=listing_id).all()

    # Prepare response data
    offers_data = [
        {
            'offer_id': offer.id,
            'buyer_id': offer.buyer_id,
            'offer_price': offer.offer_price,
            'offer_message': offer.offer_message,
            'status': offer.status,
            'created_at': offer.created_at
        }
        for offer in offers
    ]

    return jsonify({'offers': offers_data}), 200

@offers_bp.route('/get_my_offers', methods=['GET'])
# @login_required
def get_my_offers():
    """
    Fetch all offers made by a specific buyer.
    """
    user_id = request.args.get('user_id')  # Buyer's user ID

    # Fetch the buyer
    buyer = User.query.get(user_id)
    if not buyer or buyer.role.role_name != 'Buyer':
        return jsonify({'error': 'Invalid user or role'}), 403

    # Fetch all offers made by the buyer
    offers = Offer.query.filter_by(buyer_id=buyer.id).all()

    # Prepare response data
    offers_data = [
        {
            'offer_id': offer.id,
            'listing_id': offer.listing_id,
            'offer_price': offer.offer_price,
            'offer_message': offer.offer_message,
            'status': offer.status,
            'created_at': offer.created_at
        }
        for offer in offers
    ]

    return jsonify({'offers': offers_data}), 200

@offers_bp.route('/submit_offer', methods=['POST'])
# @login_required
def submit_offer():
    """
    Buyer submits an offer for a listing.
    """
    data = request.get_json()
    user_id = data.get('user_id')  # Buyer ID
    listing_id = data.get('listing_id')  # Listing ID
    offer_price = data.get('offer_price')  # Offer price
    offer_message = data.get('offer_message')  # Additional message from the buyer

    # Validate inputs
    if not (user_id and listing_id and offer_price):
        return jsonify({'error': 'user_id, listing_id, and offer_price are required'}), 400

    # Fetch the buyer and listing
    buyer = User.query.get(user_id)
    listing = Listing.query.get(listing_id)

    if not buyer or buyer.role.role_name != 'Buyer':
        return jsonify({'error': 'Invalid buyer or user role'}), 403

    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    # Ensure the offer price is greater than 0
    if offer_price <= 0:
        return jsonify({'error': 'Offer price must be greater than 0'}), 400

    # Create a new offer
    new_offer = Offer(
        listing_id=listing.id,
        buyer_id=buyer.id,
        offer_price=offer_price,
        offer_message=offer_message,
        status='Pending'  # Default status for new offers
    )
    
    db.session.add(new_offer)
    db.session.commit()

    return jsonify({'message': 'Offer submitted successfully', 'offer_id': new_offer.id}), 201

@offers_bp.route('/respond_offer', methods=['POST'])
# @login_required
def respond_offer():
    """
    Seller accepts or rejects an offer, and the status of other offers on the listing is updated accordingly.
    If an offer is accepted, the listing's status is updated to "Closed".
    """
    data = request.get_json()
    user_id = data.get('user_id')  # Seller's user ID
    offer_id = data.get('offer_id')  # Offer ID to respond to
    action = data.get('action')  # Action: "accept" or "reject"

    # Validate inputs
    if not (user_id and offer_id and action):
        return jsonify({'error': 'user_id, offer_id, and action (accept/reject) are required'}), 400

    # Fetch the seller and offer
    seller = User.query.get(user_id)
    offer = Offer.query.get(offer_id)

    if not seller or seller.role.role_name != 'Seller':
        return jsonify({'error': 'Invalid seller or user role'}), 403

    if not offer:
        return jsonify({'error': 'Offer not found'}), 404

    listing = offer.listing

    # Ensure the seller owns the listing
    if listing.seller_id != seller.id:
        return jsonify({'error': 'You can only respond to offers for your own listings'}), 403

    # Handle accepting or rejecting the offer
    if action == 'accept':
        # Update the accepted offer status
        offer.status = 'Accepted'

        # Update the listing status to "Closed"
        listing.status = 'Closed'

        # Set all other offers for this listing to inactive/rejected
        other_offers = Offer.query.filter(Offer.listing_id == listing.id, Offer.id != offer.id).all()
        for other_offer in other_offers:
            other_offer.status = 'Inactive'  # Mark other offers as inactive

        db.session.commit()

        return jsonify({
            'message': 'Offer accepted successfully',
            'offer_id': offer.id,
            'listing_status': listing.status
        }), 200

    elif action == 'reject':
        # Reject the offer
        offer.status = 'Rejected'
        db.session.commit()

        return jsonify({'message': 'Offer rejected successfully', 'offer_id': offer.id}), 200

    else:
        return jsonify({'error': 'Invalid action. Use "accept" or "reject".'}), 400
