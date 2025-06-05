-- init_db.sql

CREATE DATABASE IF NOT EXISTS fastapi_users CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'fastapi_user'@'localhost' IDENTIFIED BY 'YourStrongPassword123!';

GRANT ALL PRIVILEGES ON fastapi_users.* TO 'fastapi_user'@'localhost';

FLUSH PRIVILEGES;
