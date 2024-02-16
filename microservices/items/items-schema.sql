-- Create users table
CREATE TABLE IF NOT EXISTS items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(50) NOT NULL,
  item_name VARCHAR(50) NOT NULL,
  description VARCHAR(255) NOT NULL,
  watch_reference_number VARCHAR(10) NOT NULL,
  watch_model VARCHAR(255) NOT NULL,
  watch_year YEAR NOT NULL,
  brand VARCHAR(100) NOT NULL,
  item_image LONGBLOB,
  auction_won TINYINT(1) NOT NULL,
  bid_amount INT NOT NULL,
  starting_price INT NOT NULL,
  item_condition VARCHAR(50) NOT NULL,
  auction_start DATETIME NOT NULL,
  auction_deadline DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS brands (
  id INT AUTO_INCREMENT PRIMARY KEY,
  brand_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS purchases (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  item_id INT NOT NULL,
  status VARCHAR(20) NOT NULL,
  purchase_date DATETIME NOT NULL,
  purchase_amount INT NOT NULL
);

INSERT INTO brands (brand_name) VALUES
('Rolex'),
('Patek Philippe'),
('Audemars Piguet'),
('Omega'),
('Cartier'),
('TAG Heuer'),
('Breitling'),
('Hublot'),
('IWC Schaffhausen'),
('Jaeger-LeCoultre'),
('Panerai'),
('Vacheron Constantin');