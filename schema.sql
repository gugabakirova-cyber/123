DROP DATABASE IF EXISTS cafe_system;
CREATE DATABASE cafe_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cafe_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    category VARCHAR(80) NOT NULL DEFAULT 'Без категории',
    unit VARCHAR(20) NOT NULL DEFAULT 'шт',
    purchase_price DECIMAL(12,2) NOT NULL DEFAULT 0,
    sale_price DECIMAL(12,2) NOT NULL DEFAULT 0,
    quantity DECIMAL(12,2) NOT NULL DEFAULT 0,
    min_quantity DECIMAL(12,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity DECIMAL(12,2) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    category VARCHAR(80) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_movements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    movement_type VARCHAR(30) NOT NULL,
    quantity DECIMAL(12,2) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

INSERT INTO users (username, password, role)
VALUES ('admin', 'admin', 'admin');

INSERT INTO products 
(name, category, unit, purchase_price, sale_price, quantity, min_quantity)
VALUES
('Кофе зерновой', 'Напитки', 'кг', 6500, 12000, 5, 2),
('Молоко', 'Сырье', 'л', 500, 900, 12, 5),
('Сахар', 'Сырье', 'кг', 400, 700, 10, 3),
('Сироп ванильный', 'Сиропы', 'л', 2000, 4500, 3, 1),
('Стакан бумажный 400 мл', 'Расходники', 'шт', 35, 80, 100, 30);

INSERT INTO expenses
(title, category, amount, comment)
VALUES
('Аренда помещения', 'Постоянные расходы', 250000, 'Ежемесячная аренда'),
('Коммунальные услуги', 'Постоянные расходы', 45000, 'Электричество и вода'),
('Закуп продуктов', 'Сырье', 80000, 'Первичная закупка');