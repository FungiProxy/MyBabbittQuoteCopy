-- Drop existing table and indexes
DROP TABLE IF EXISTS options;

-- Create new options table with correct schema
CREATE TABLE options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    description TEXT,
    price FLOAT NOT NULL DEFAULT 0.0,
    price_type VARCHAR DEFAULT 'fixed',
    category VARCHAR,
    product_families VARCHAR,
    excluded_products VARCHAR,
    choices JSON,
    adders JSON,
    rules JSON
);

-- Create indexes
CREATE INDEX ix_options_category ON options (category);
CREATE INDEX ix_options_id ON options (id);
CREATE INDEX ix_options_name ON options (name); 