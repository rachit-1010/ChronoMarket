CREATE TABLE Auctions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    item_id INT NOT NULL,
    item_name VARCHAR(255),
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    status ENUM('pending', 'live', 'closed') NOT NULL DEFAULT 'pending'
);