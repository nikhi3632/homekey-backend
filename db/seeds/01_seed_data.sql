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
    ('Yuchen Zhang', 'yuchen@test.com', '$2b$12$/1e2PQbS5F5XfQQ8/hydiOCijgES3vJ.o74RJb6zI3qXRN0K0TxW.', 2);

-- Seed Listings
INSERT INTO Listings (id, seller_id, title, price, description, address, status, created_at, bedrooms, bathrooms, squareFootage) VALUES
(1, 1, 'Beautiful 4-bedroom house', 850000.00, 'Spacious 4-bedroom house with garden', '123 Main Street, CA 90001', 'Pending Approval', '2024-12-04 23:50:45.202', 3, 3, 1450),
(2, 2, 'Luxury 2-bedroom apartment', 550000.00, 'Modern 2-bedroom apartment in the city center', '456 Elm Street, CA 94105', 'Pending Approval', '2024-12-04 23:50:45.202', 3, 2, 1250),
(3, 3, 'Cozy 3-bedroom cottage', 420000.00, 'Charming 3-bedroom cottage with a large backyard', '789 Oak Street, CA 90210', 'Pending Approval', '2024-12-04 23:50:45.202', 2, 2, 1000),
(4, 5, 'Modern 3-Bedroom Apartment', 200000.00, 'A modern 3-bedroom apartment with updated amenities.', '123 Maple St, Springfield, USA 62704', 'Approved', '2024-12-05 10:18:59.648', 2, 1, 1000),
(5, 5, 'Luxury 5-Bedroom Villa', 400000.00, 'A luxury villa featuring a swimming pool and a private garden.', '456 Elm St, Beverly Hills, USA 90210', 'Approved', '2024-12-05 10:18:59.648', 2, 1, 1000),
(6, 5, 'Cozy 2-Bedroom House', 600000.00, 'A cozy 2-bedroom house in a quiet neighborhood.', '789 South Pine Rd, Austin, USA 78701', 'Approved', '2024-12-05 10:18:59.648', 3, 2, 2000),
(7, 5, 'Spacious 4-Bedroom Townhouse', 800000.00, 'A spacious townhouse with modern interiors and large backyard.', '321 Oak Ave, Seattle, USA 98101', 'Approved', '2024-12-05 10:18:59.648', 3, 2, 2000),
(8, 5, 'Charming Cottage', 1000000.00, 'A charming cottage with a beautiful view and lush greenery.', '654 Willow Lane, Portland, USA 97201', 'Approved', '2024-12-05 10:18:59.648', 3, 2, 2000),
(9, 5, 'Downtown Studio Apartment', 1200000.00, 'A stylish studio apartment located in the heart of downtown.', '987 Market St, San Francisco, USA 94105', 'Approved', '2024-12-05 10:18:59.648', 5, 4, 3500),
(10, 5, 'Beachfront Condo', 1400000.00, 'A beachfront condo with stunning ocean views and amenities.', '111 Ocean Dr, Miami, USA 33101', 'Approved', '2024-12-05 10:18:59.648', 5, 4, 3500),
(11, 5, 'Mountain Retreat', 1600000.00, 'A peaceful mountain retreat perfect for a weekend getaway.', '222 Aspen Way, Denver, USA 80202', 'Approved', '2024-12-05 10:18:59.648', 5, 4, 3500),
(12, 5, 'Historic 6-Bedroom Mansion', 1800000.00, 'A historic mansion with elegant architecture and design.', '333 Heritage Rd, Charleston, USA 29401', 'Approved', '2024-12-05 10:18:59.648', 5, 4, 3500),
(13, 5, 'Suburban Family Home', 1900000.00, 'A family-friendly home in a quiet suburban area.', '444 Maple Ct, Chicago, USA 60601', 'Approved', '2024-12-05 10:18:59.648', 5, 4, 3500),
(14, 5, 'Modern Loft', 1950000.00, 'A modern loft with high ceilings and industrial aesthetics.', '555 Warehouse Blvd, New York, USA 10001', 'Approved', '2024-12-05 10:18:59.648', 5, 4, 3500),
(15, 5, 'Elegant Penthouse', 2000000.00, 'An elegant penthouse offering panoramic city views.', '666 Skyline Ave, Los Angeles, USA 90001', 'Approved', '2024-12-05 10:18:59.648', 5, 4, 3500);

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
