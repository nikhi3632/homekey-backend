from flask import Blueprint, request, jsonify
from app.models import db, User, Listing, Offer
from utils import login_required

# Create a Blueprint for offers
offers_bp = Blueprint('offers', __name__)

# POST /offers/
@offers_bp.route('/offers/', methods=['POST'])
def create_offer():
    data = request.get_json()
    new_offer = Offer(**data)
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
    return jsonify([offer.to_dict() for offer in offers])

# GET /offers/{buyer_id}
@offers_bp.route('/offers/buyer/<int:buyer_id>', methods=['GET'])
def get_offer_by_buyer(buyer_id):
    offers = Offer.query.filter_by(buyer_id=buyer_id).all()
    return jsonify([offer.to_dict() for offer in offers])

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
    return jsonify({'id': id, 'action': action})
