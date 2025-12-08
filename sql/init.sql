CREATE DATABASE IF NOT EXISTS comparateur
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE comparateur;

CREATE TABLE IF NOT EXISTS phones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    website VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'EUR',
    product_url TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO phones (phone_name, brand, website, price, currency, product_url)
VALUES ('iPhone 15', 'Apple', 'Site1', 1099.00, 'EUR', 'https://exemple.com/iphone15');

INSERT INTO phones (phone_name, brand, website, price, currency, product_url)
VALUES ('Galaxy S24', 'Samsung', 'Site2', 879.00, 'EUR', 'https://exemple.com/galaxys24');

INSERT INTO phones (phone_name, brand, website, price, currency, product_url)
VALUES ('iPhone 15', 'Apple', 'Site2', 1209.00, 'EUR', 'https://exemple.com/iphone15');