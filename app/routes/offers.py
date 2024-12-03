from flask import Blueprint, request, jsonify
from app.models import db, User, Listing, Offer
from app.utils import login_required

# Create a Blueprint for offers
offers_bp = Blueprint('offers', __name__)

# POST /offers/
@offers_bp.route('/create_offer/', methods=['POST'])
@login_required
def create_offer():
    listing_id = request.json.get('listing_id')
    buyer_id = request.json.get('buyer_id')
    offer_price = request.json.get('offer_price')

    if not (listing_id and buyer_id and offer_price):
        return jsonify({'error': 'All fields are required'}), 400

    new_offer = Offer(listing_id=listing_id, buyer_id=buyer_id, offer_price=offer_price)
    db.session.add(new_offer)
    db.session.commit()

    return jsonify({'message': 'Offer created', 'offer_id': new_offer.id}), 201

# GET /offers/{listing_id}
@offers_bp.route('/get_offers_by_listing', methods=['GET'])
@login_required
def get_offers_by_listing():
    listing_id = request.args.get('listing_id')
    if not listing_id:
        return jsonify({'error': 'listing_id is required'}), 400
    offers = Offer.query.filter_by(listing_id=listing_id).all()
    if not offers:
        return jsonify({'error': 'No offers found for this listing'}), 404
    return jsonify([offer.to_dict() for offer in offers])

# GET /offers/{buyer_id}
@offers_bp.route('/get_my_offers', methods=['GET'])
@login_required
def get_my_offers():
    user_id = request.args.get('user_id')

    # Fetch the user (Buyer)
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Ensure the user is a Buyer
    if user.role.role_name != 'Buyer':
        return jsonify({'error': 'Only Buyers can view their own offers'}), 403

    # Fetch offers where the buyer_id matches the user's ID
    offers = Offer.query.filter_by(buyer_id=user_id).all()

    # Prepare response data
    offers_data = [
        {
            'id': offer.id,
            'listing_id': offer.listing_id,
            'buyer_id': offer.buyer_id,
            'offer_price': offer.offer_price,
            'status': offer.status,
            'created_at': offer.created_at
        }
        for offer in offers
    ]

    return jsonify(offers_data), 200

# PUT /offers/{id}/(accept, reject)
@offers_bp.route('/decide_offer', methods=['PUT'])
@login_required
def decide_offer():
    offer_id = request.json.get('offer_id')
    action = request.json.get('action')
    user_id = request.json.get('user_id')

    if not (offer_id and action and user_id):
        return jsonify({'error': 'offer_id, action, and user_id are required'}), 400

    # Fetch the offer
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'error': 'Offer not found'}), 404

    listing = Listing.query.get(offer.listing_id)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    # Ensure the user is the seller of the listing
    if listing.seller_id != user_id:
        return jsonify({'error': 'You are not the seller of this listing'}), 403

    if action == 'accept':
        # Update the listing's status to 'Sold' and the offer's status to 'Accepted'
        listing = Listing.query.get(offer.listing_id)
        listing.status = 'Sold'
        offer.status = 'Accepted'
    elif action == 'reject':
        # Update the offer's status to 'Rejected'
        offer.status = 'Rejected'    
    else:
        return jsonify({'error': 'Invalid action'}), 400    

    db.session.commit()
    return jsonify({'message': 'Offer updated'}), 200