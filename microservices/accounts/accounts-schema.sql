-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  UNIQUE(username),
  password VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  api_key VARCHAR(100) NOT NULL,
  admin_account BOOLEAN,
  suspended BOOLEAN
);

-- Create favorites table
CREATE TABLE IF NOT EXISTS watchlist (
  id INT AUTO_INCREMENT PRIMARY KEY,
  api_key VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  watchlist_item VARCHAR(100) NOT NULL -- will be a watch reference #
);

CREATE TABLE IF NOT EXISTS blocked_users (
  email VARCHAR(50) PRIMARY KEY,
  blocked BOOLEAN
);