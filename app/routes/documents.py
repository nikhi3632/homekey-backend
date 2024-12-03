import base64

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
