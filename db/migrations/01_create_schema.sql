-- Create custom ENUM types
CREATE TYPE role_type AS ENUM ('Seller', 'Buyer', 'FSH');
CREATE TYPE listing_status AS ENUM ('Available', 'In Escrow', 'Sold');
CREATE TYPE offer_status AS ENUM ('Pending', 'Accepted', 'Rejected');
CREATE TYPE document_type AS ENUM ('Disclosure', 'Contract', 'Inspection Report');
CREATE TYPE escrow_status AS ENUM ('Open', 'Closed');
CREATE TYPE payment_status AS ENUM ('Pending', 'Succeeded', 'Failed', 'Cancelled');

-- Create Users table
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    task_progress JSONB DEFAULT '{}'::jsonb
);

-- Create Roles table
CREATE TABLE Roles (
    id SERIAL PRIMARY KEY,
    role_name role_type
);

-- Create UserRoles table
CREATE TABLE UserRoles (
    user_id INT REFERENCES Users(id) ON DELETE CASCADE,
    role_id INT REFERENCES Roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- Create Listings table
CREATE TABLE Listings (
    id SERIAL PRIMARY KEY,
    seller_id INT REFERENCES Users(id) ON DELETE SET NULL,
    title VARCHAR(255),
    price NUMERIC(10, 2),
    description TEXT,
    address TEXT,
    status listing_status DEFAULT 'Available',
    photos JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Offers table
CREATE TABLE Offers (
    id SERIAL PRIMARY KEY,
    listing_id INT REFERENCES Listings(id) ON DELETE CASCADE,
    buyer_id INT REFERENCES Users(id) ON DELETE SET NULL,
    offer_price NUMERIC(10, 2),
    status offer_status DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Documents table
CREATE TABLE Documents (
    id SERIAL PRIMARY KEY,
    listing_id INT REFERENCES Listings(id) ON DELETE CASCADE,
    uploaded_by INT REFERENCES Users(id) ON DELETE SET NULL,
    document_type document_type,
    file_url TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Escrow table
CREATE TABLE Escrow (
    id SERIAL PRIMARY KEY,
    listing_id INT REFERENCES Listings(id) ON DELETE CASCADE,
    buyer_id INT REFERENCES Users(id) ON DELETE SET NULL,
    fsh_id INT REFERENCES Users(id) ON DELETE SET NULL,
    status escrow_status DEFAULT 'Open',
    deposit_amount NUMERIC(10, 2),
    stripe_payment_intent_id VARCHAR(255),
    stripe_payment_status payment_status DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_user_email ON Users(email);
CREATE INDEX idx_listing_status ON Listings(status);
CREATE INDEX idx_offer_status ON Offers(status);
CREATE INDEX idx_escrow_status ON Escrow(status);
