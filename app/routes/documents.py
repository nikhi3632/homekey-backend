import base64
from flask import Blueprint, request, jsonify
from app.models import db, User, Listing, Document 
from app.utils import login_required

documents_bp = Blueprint('documents', __name__)

def format_document(document):
    """
    Format a document's data for inclusion in the listing response with Base64 encoded file content.
    """
    # Encode file data as Base64
    file_content_base64 = base64.b64encode(document.file_data).decode('utf-8')
    
    return {
        'id': document.id,
        'document_type': document.document_type,
        'file_name': document.file_name,
        'uploaded_by': document.uploaded_by,
        'uploaded_at': document.uploaded_at,
        'file_content': file_content_base64  # Include Base64 encoded file content
    }

@documents_bp.route('/gather_disclosure_documents', methods=['POST'])
#@login_required
def gather_disclosure_documents():
    """
    FSH agent uploads disclosure documents for a listing.
    """
    file = request.files.get('document')  # File upload
    user_id = request.form.get('user_id')  # FSH agent's ID
    listing_id = request.form.get('listing_id')  # Listing ID

    # Validate inputs
    if not (file and user_id and listing_id):
        return jsonify({'error': 'Document, user_id, and listing_id are required'}), 400

    # Fetch the FSH agent and listing
    user = User.query.get(user_id)
    listing = Listing.query.get(listing_id)

    if not user or user.role.role_name != 'FSH':
        return jsonify({'error': 'Only FSH agents can upload disclosure documents'}), 403

    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    # Save the document to the Documents table
    file_name = file.filename
    file_data = file.read()

    new_document = Document(
        listing_id=listing.id,
        uploaded_by=user.id,
        document_type='Disclosure',
        file_name=file_name,
        file_data=file_data
    )
    db.session.add(new_document)
    db.session.commit()

    # Update task progress for the FSH
    task_progress = user.task_progress.get('FSH', {})
    task_progress['gather_disclosure_documents'] = True
    user.task_progress['FSH'] = task_progress

    # Save changes to the database
    db.session.commit()

    # Return success response
    return jsonify({'message': 'Disclosure document uploaded successfully', 'document_id': new_document.id}), 201
