-- Seed Roles
INSERT INTO Roles (role_name) VALUES
    ('Seller'),
    ('Buyer'),
    ('FSH');

-- Seed Users (passwords are 'password123' hashed)
INSERT INTO Users (name, email, password_hash, role_id) VALUES
    ('John Seller', 'seller@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFyGQllxW2H3kxW', 1),  -- Seller role (role_id = 1)
    ('Jane Buyer', 'buyer@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFyGQllxW2H3kxW', 2),   -- Buyer role (role_id = 2)
    ('FSH Agent', 'fsh@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFyGQllxW2H3kxW', 3);    -- FSH role (role_id = 3)

-- Seed Listings
INSERT INTO Listings (seller_id, title, price, description, address, status) VALUES
(1, 'Beautiful 4-bedroom house', 850000, 'Spacious 4-bedroom house with garden', '123 Main Street, CA', 'Pending Approval'),
(2, 'Luxury 2-bedroom apartment', 550000, 'Modern 2-bedroom apartment in the city center', '456 Elm Street, CA', 'Pending Approval'),
(3, 'Cozy 3-bedroom cottage', 420000, 'Charming 3-bedroom cottage with a large backyard', '789 Oak Street, CA', 'Pending Approval');

-- Seed Offers
INSERT INTO Offers (listing_id, buyer_id, offer_price, status) VALUES
    (1, 2, 440000.00, 'Pending'),
    (2, 2, 245000.00, 'Pending');

-- -- Seed Documents
-- INSERT INTO Documents (listing_id, uploaded_by, document_type, file_url) VALUES
--     (1, 1, 'Disclosure', 'https://example.com/documents/disclosure1.pdf'),
--     (1, 3, 'Inspection Report', 'https://example.com/documents/inspection1.pdf');

-- Seed Escrow
-- INSERT INTO Escrow (listing_id, buyer_id, fsh_id, status, deposit_amount, stripe_payment_intent_id, stripe_payment_status) VALUES
--     (1, 2, 3, 'Open', 44000.00, 'pi_123456789', 'Pending');
