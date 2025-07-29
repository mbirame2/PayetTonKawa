CREATE TABLE Product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    quantity INT NOT NULL
);

INSERT INTO Product (name, price, description, quantity) VALUES
('Produit A', 19.99, 'Description du produit A', 100),
('Produit B', 29.99, 'Description du produit B', 150),
('Produit C', 39.99, 'Description du produit C', 200),
('Produit D', 49.99, 'Description du produit D', 250),
('Produit E', 59.99, 'Description du produit E', 300);
