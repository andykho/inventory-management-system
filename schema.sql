CREATE DATABASE inventory_db;
USE inventory_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff') NOT NULL DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_code VARCHAR(50) NOT NULL UNIQUE,
    product_name VARCHAR(100) NOT NULL,
    current_stock INT NOT NULL DEFAULT 0,
    minimum_stock INT NOT NULL DEFAULT 0,
    supplier_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (supplier_id)
    REFERENCES suppliers(id)
);

CREATE TABLE stock_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    transaction_type ENUM('IN', 'OUT') NOT NULL,
    quantity INT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id)
        REFERENCES products(id),

    FOREIGN KEY (user_id)
        REFERENCES users(id)
);

INSERT INTO users
(username, password, role)
VALUES
('admin', 'admin123', 'admin');

INSERT INTO suppliers (name, phone, address)
VALUES
('Logitech Indonesia', '021111111', 'Jakarta'),
('Samsung Indonesia', '021222222', 'Jakarta'),
('HyperX Indonesia', '021333333', 'Jakarta');

INSERT INTO products (
    product_code,
    product_name,
    current_stock,
    minimum_stock,
    supplier_id
)
VALUES
('KB001', 'Logitech G Pro Keyboard', 50, 10, 1),
('MS001', 'Logitech G102 Mouse', 30, 10, 1),
('SSD001', 'Samsung 970 EVO SSD', 15, 5, 2);