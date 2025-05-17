-- Drop tables if they exist
DROP TABLE IF EXISTS products;

-- Create the products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    price TEXT NOT NULL,
    image TEXT NOT NULL
);

-- Drop orders table if it exists
DROP TABLE IF EXISTS orders;

-- Create the orders table with an additional payment_method column
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price TEXT NOT NULL,  -- Ensure price is stored as TEXT
    payment_method TEXT NOT NULL,
    bitcoin_address TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
