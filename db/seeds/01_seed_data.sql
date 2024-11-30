-- Seed Roles
INSERT INTO Roles (role_name) VALUES
    ('Seller'),
    ('Buyer'),
    ('FSH');

-- Seed Users (passwords are 'password123' hashed)
INSERT INTO Users (name, email, password_hash) VALUES
    ('John Seller', 'seller@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFyGQllxW2H3kxW'),
    ('Jane Buyer', 'buyer@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFyGQllxW2H3kxW'),
    ('FSH Agent', 'fsh@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFyGQllxW2H3kxW');

-- Assign Roles to Users
INSERT INTO UserRoles (user_id, role_id) VALUES
    (1, 1), -- John is a Seller
    (2, 2), -- Jane is a Buyer
    (3, 3); -- FSH Agent is FSH

-- Seed Listings
INSERT INTO Listings (seller_id, title, price, description, address, status, photos) VALUES
    (1, 'Beautiful 3BR House', 450000.00, 'Spacious 3 bedroom house with modern amenities', '123 Main St, Anytown, USA', 'Available', '{"photos": ["photo1.jpg", "photo2.jpg"]}'),
    (1, 'Cozy 2BR Apartment', 250000.00, 'Well-maintained 2 bedroom apartment in the city center', '456 Oak Ave, Anytown, USA', 'Available', '{"photos": ["photo3.jpg", "photo4.jpg"]}');

-- Seed Offers
INSERT INTO Offers (listing_id, buyer_id, offer_price, status) VALUES
    (1, 2, 440000.00, 'Pending'),
    (2, 2, 245000.00, 'Pending');

-- Seed Documents
INSERT INTO Documents (listing_id, uploaded_by, document_type, file_url) VALUES
    (1, 1, 'Disclosure', 'https://example.com/documents/disclosure1.pdf'),
    (1, 3, 'Inspection Report', 'https://example.com/documents/inspection1.pdf');

-- Seed Escrow
INSERT INTO Escrow (listing_id, buyer_id, fsh_id, status, deposit_amount, stripe_payment_intent_id, stripe_payment_status) VALUES
    (1, 2, 3, 'Open', 44000.00, 'pi_123456789', 'Pending');
