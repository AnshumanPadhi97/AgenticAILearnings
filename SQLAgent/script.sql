-- Create schema
CREATE SCHEMA ecommerce;

-- Products table
CREATE TABLE ecommerce.products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INTEGER,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE ecommerce.customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    city VARCHAR(50),
    country VARCHAR(50)
);

-- Orders table
CREATE TABLE ecommerce.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES ecommerce.customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending'
);

-- Order items table
CREATE TABLE ecommerce.order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES ecommerce.orders(order_id),
    product_id INTEGER REFERENCES ecommerce.products(product_id),
    quantity INTEGER,
    unit_price DECIMAL(10,2)
);

-- Insert sample data
INSERT INTO ecommerce.products (product_name, category, price, stock_quantity) VALUES
('Laptop Pro 15', 'Electronics', 1299.99, 25),
('Wireless Headphones', 'Electronics', 199.99, 100),
('Coffee Maker', 'Home & Kitchen', 89.99, 50),
('Running Shoes', 'Sports', 129.99, 75),
('Smartphone', 'Electronics', 699.99, 30),
('Desk Chair', 'Furniture', 249.99, 20),
('Water Bottle', 'Sports', 19.99, 200),
('Book: Data Science', 'Books', 39.99, 40);

INSERT INTO ecommerce.customers (first_name, last_name, email, city, country) VALUES
('John', 'Smith', 'john.smith@email.com', 'New York', 'United States'),
('Sarah', 'Johnson', 'sarah.j@email.com', 'Toronto', 'Canada'),
('Mike', 'Brown', 'mike.brown@email.com', 'London', 'United Kingdom'),
('Emma', 'Davis', 'emma.davis@email.com', 'Sydney', 'Australia'),
('David', 'Wilson', 'david.w@email.com', 'Berlin', 'Germany');

INSERT INTO ecommerce.orders (customer_id, total_amount, status) VALUES
(1, 1499.98, 'completed'),
(2, 219.98, 'completed'),
(3, 89.99, 'pending'),
(1, 149.99, 'shipped'),
(4, 939.98, 'completed');

INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1299.99),
(1, 2, 1, 199.99),
(2, 2, 1, 199.99),
(2, 7, 1, 19.99),
(3, 3, 1, 89.99),
(4, 4, 1, 129.99),
(5, 5, 1, 699.99),
(5, 6, 1, 249.99);
