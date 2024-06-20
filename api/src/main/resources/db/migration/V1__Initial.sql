CREATE TABLE IF NOT EXISTS users (
    id int PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS videos (
    id int PRIMARY KEY AUTO_INCREMENT,
    bucket VARCHAR(255) NOT NULL,
    _key VARCHAR(255) NOT NULL,
    uploaded_by int,
    CONSTRAINT fk_user FOREIGN KEY (uploaded_by) REFERENCES users(id)
);