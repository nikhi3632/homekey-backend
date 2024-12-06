-- Roles table
CREATE TABLE Roles (
    id SERIAL PRIMARY KEY,              -- Auto-incremented ID
    role_name VARCHAR(50) UNIQUE NOT NULL -- Unique role name (e.g., "Buyer", "Seller")
);

-- Create Users table
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    task_progress JSONB DEFAULT '{}'::jsonb,
    role_id INT NOT NULL,                -- Foreign key to the Roles table (One role per user)
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE  -- Ensures referential integrity
);

CREATE TABLE Listings (
    id SERIAL PRIMARY KEY,                     -- Unique ID for the listing
    seller_id INT REFERENCES Users(id) ON DELETE SET NULL,  -- Reference to the seller's user ID
    title VARCHAR(255) NOT NULL,              -- Title of the listing
    price NUMERIC(10, 2) NOT NULL,            -- Price of the property
    description TEXT,                         -- Description of the property
    address TEXT,                             -- Address of the property
    status VARCHAR(50) DEFAULT 'Pending Approval', -- Status of the listing (Pending Approval, Approved, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the listing was created
    bedrooms INT,
    bathrooms INT,
    squarefootage INT,
);

-- Create Offers table
CREATE TABLE Offers (
    id SERIAL PRIMARY KEY,
    listing_id INT REFERENCES Listings(id) ON DELETE CASCADE,  -- Reference to the listing
    buyer_id INT REFERENCES Users(id) ON DELETE SET NULL,  -- Reference to the buyer
    offer_price NUMERIC(10, 2) NOT NULL,  -- Offered price
    offer_message TEXT,  -- Message from the buyer
    status VARCHAR(50) DEFAULT 'Pending',  -- Offer status (Pending, Accepted, Rejected, Inactive)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp for when the offer was created
);


CREATE TABLE Documents (
    id SERIAL PRIMARY KEY,                     -- Unique ID for the document
    listing_id INT REFERENCES Listings(id) ON DELETE CASCADE, -- Reference to the related listing
    uploaded_by INT REFERENCES Users(id) ON DELETE SET NULL, -- User who uploaded the document
    document_type VARCHAR(50) NOT NULL,        -- Type of document (e.g., Notification, Disclosure, Photo)
    file_name VARCHAR(255) NOT NULL,           -- Original file name
    file_data BYTEA NOT NULL,                  -- Binary data of the file
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for upload
);

-- -- Create Escrow table
CREATE TABLE Escrow (
    id SERIAL PRIMARY KEY,                     -- Unique ID for the escrow record
    listing_id INT REFERENCES Listings(id) ON DELETE CASCADE, -- Reference to the related listing
    seller_id INT REFERENCES Users(id) ON DELETE SET NULL,    -- Reference to the seller
    escrow_number VARCHAR(50) NOT NULL,        -- Unique escrow number
    status VARCHAR(50) DEFAULT 'Open',         -- Escrow status (Open, Closed, Cancelled)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when escrow was opened
);

-- Create indexes for better query performance
CREATE INDEX idx_user_email ON Users(email);
CREATE INDEX idx_listing_status ON Listings(status);
CREATE INDEX idx_listing_id ON Offers(listing_id);
CREATE INDEX idx_buyer_id ON Offers(buyer_id);
