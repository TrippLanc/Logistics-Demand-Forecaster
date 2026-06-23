-- Dropping tables if they exist to allow clean re-runs of the script
DROP TABLE IF EXISTS fulfillment CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- 1. Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_fname VARCHAR(50),
    customer_lname VARCHAR(50),
    customer_city VARCHAR(100),
    customer_state VARCHAR(50),
    customer_zipcode VARCHAR(20),
    customer_street VARCHAR(255)
);

-- 2. Categories Table
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100)
);

-- 3. Products Table
CREATE TABLE products (
    product_card_id INT PRIMARY KEY,
    product_name VARCHAR(150),
    category_id INT REFERENCES categories(category_id),
    product_price DECIMAL(10,2)
);

-- 4. Orders Table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date_dateorders TIMESTAMP,
    order_status VARCHAR(50),
    shipping_mode VARCHAR(50),
    market VARCHAR(50),
    order_region VARCHAR(100)
);

-- 5. Order Items Table
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_card_id INT REFERENCES products(product_card_id),
    order_item_quantity INT,
    order_item_product_price DECIMAL(10,2),
    order_item_discount DECIMAL(10,2),
    order_item_total DECIMAL(10,2)
);

-- 6. Fulfillment & Logistics Table
CREATE TABLE fulfillment (
    fulfillment_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    days_for_shipping_real INT,
    days_for_shipment_scheduled INT,
    delivery_status VARCHAR(50),
    late_delivery_risk INT
);

-- Indexes for quick lookups and downstream ML features
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_fulfillment_order ON fulfillment(order_id);
CREATE INDEX idx_fulfillment_risk ON fulfillment(late_delivery_risk);