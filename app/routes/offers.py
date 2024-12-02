from flask import Blueprint, request, jsonify
from app.models import Offer
from app import db

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
@offers_bp.route('/offers/listing/<int:listing_id>', methods=['GET'])
def get_offer_by_listing(listing_id):
    offers = Offer.query.filter_by(listing_id=listing_id).all()
    return jsonify([offer.to_dict() for offer in offers])

# GET /offers/{buyer_id}
@offers_bp.route('/offers/buyer/<int:buyer_id>', methods=['GET'])
def get_offer_by_buyer(buyer_id):
    offers = Offer.query.filter_by(buyer_id=buyer_id).all()
    return jsonify([offer.to_dict() for offer in offers])

# PUT /offers/{id}/(accept, reject)
@offers_bp.route('/offers/<int:id>/<action>', methods=['PUT'])
def update_offer(id, action):
    if action not in ['accept', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400
    offer = Offer.query.get(id)
    if not offer:
        return jsonify({'error': 'Offer not found'}), 404
    offer.status = action
    db.session.commit()
    return jsonify({'id': id, 'action': action})
