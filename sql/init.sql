CREATE DATABASE IF NOT EXISTS comparateur;
USE comparateur;

CREATE TABLE site (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    url VARCHAR(255)
);

CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE offer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    site_id INT,
    product_name_raw VARCHAR(255),
    price DECIMAL(10,2),
    product_url VARCHAR(500),
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (site_id) REFERENCES site(id)
);
