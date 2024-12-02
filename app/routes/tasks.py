
#TODO: change the structure on discussion with the frontend team

TASK_SEQUENCES = {
    'Seller': [
        'notify_fsh_of_intent_to_sell',
        'prepare_home_for_listing',
        'provide_photo_for_listing',
        'create_listing',
        'approve_listing',
        'gather_disclosures',
        'respond_to_buyers',
        'sign_purchase_contract',
        'submit_deposit',
        'close_escrow'
    ],
    'Buyer': [
        'search_properties',
        'submit_offer',
        'review_disclosures',
        'schedule_inspection',
        'transfer_deposit',
        'final_walkthrough',
        'close_escrow'
    ],
    'FSH': [
        'approve_listing',
        'order_appraisal',
        'approve_contract',
        'transfer_loan_funds',
        'close_escrow'
    ]
}
