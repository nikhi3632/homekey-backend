
#TODO: verify

TASK_SEQUENCES = {
    'Seller': [
        'notify_fsh_intent_to_sell',
        'prepare_home_for_listing',
        'provide_photo_for_listing',
        'enter_sale_listing_in_fsh',
        'order_natural_hazards_report',
        'respond_to_interested_buyers',
        'sign_or_counter_offer',
        'finalize_purchase_contract',
        'schedule_appraisal_appointment',
        'order_termite_inspection',
        'schedule_termite_appointment',
        'schedule_property_inspection',
        'provide_termite_report',
        'route_documents_via_docusign',
        'complete_disclosure_documents',
        'notify_document_completion',
        'cure_section_i_items',
        'request_loan_payoff',
        'obtain_power_of_attorney',
        'schedule_title_closing',
        'schedule_final_walkthrough',
        'transfer_utilities',
        'close_escrow_and_receive_funds',
        'provide_keys'
    ],
    
    'Buyer': [
        'submit_purchase_offer',
        'finalize_purchase_contract',
        'submit_contract_to_fsh',
        'submit_deposit_to_title',
        'review_disclosure_documents',
        'order_property_inspection',
        'receive_appraisal_report',
        'route_documents_via_docusign',
        'notify_document_completion',
        'schedule_title_closing',
        'schedule_final_walkthrough',
        'transfer_utilities',
        'provide_keys'
    ],
    
    'FSH': [
        'approve_listing_in_fsh',
        'gather_disclosure_documents',
        'open_escrow',
        'order_natural_hazards_report',
        'mark_listing_in_escrow',
        'provide_access_to_disclosures',
        'order_fee_sample_appraisal',
        'order_leasehold_appraisal',
        'provide_termite_report',
        'prepare_disclosure_documents',
        'route_documents_via_docusign',
        'sign_title_documents',
        'transfer_loan_funds',
        'close_sale_listing'
    ]
}
