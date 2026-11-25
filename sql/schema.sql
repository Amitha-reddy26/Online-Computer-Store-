CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    name VARCHAR(150) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    CHECK (price >= 0),
    CHECK (stock >= 0),
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT IGNORE INTO categories VALUES
(1,'Laptops'),(2,'Accessories'),(3,'Monitors');

INSERT IGNORE INTO products VALUES
(1,1,'Dell Laptop',899.99,15),
(2,1,'MacBook Air',1099.99,10),
(3,2,'Wireless Mouse',29.99,50),
(4,2,'Mechanical Keyboard',79.99,25),
(5,3,'Samsung Monitor',249.99,20);

INSERT IGNORE INTO customers VALUES
(1,'Demo Customer','customer@example.com'),
(2,'Test Customer','test@example.com');
