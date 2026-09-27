DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at DATETIME
);

CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT,
    title VARCHAR(200),
    content TEXT,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users VALUES (1, 'Alice Johnson', 'alice@example.com', '2026-09-01 10:00:00');
INSERT INTO users VALUES (2, 'Ben Smith', 'ben@example.com', '2026-09-02 10:00:00');
INSERT INTO users VALUES (3, 'Carla Davis', 'carla@example.com', '2026-09-03 10:00:00');
INSERT INTO users VALUES (4, 'Daniel Lee', 'daniel@example.com', '2026-09-04 10:00:00');
INSERT INTO users VALUES (5, 'Emma Wilson', 'emma@example.com', '2026-09-05 10:00:00');
INSERT INTO users VALUES (6, 'Frank Miller', 'frank@example.com', '2026-09-06 10:00:00');
INSERT INTO users VALUES (7, 'Grace Brown', 'grace@example.com', '2026-09-07 10:00:00');
INSERT INTO users VALUES (8, 'Henry Taylor', 'henry@example.com', '2026-09-08 10:00:00');
INSERT INTO users VALUES (9, 'Isabella Moore', 'isabella@example.com', '2026-09-09 10:00:00');
INSERT INTO users VALUES (10, 'Jack Anderson', 'jack@example.com', '2026-09-10 10:00:00');

INSERT INTO posts VALUES (1, 1, 'First Post', 'This is my first post.', '2026-09-11 09:00:00');
INSERT INTO posts VALUES (2, 2, 'SQL Basics', 'Learning the basics of SQL.', '2026-09-12 09:00:00');
INSERT INTO posts VALUES (3, 3, 'Data Science', 'A post about data science.', '2026-09-13 09:00:00');
INSERT INTO posts VALUES (4, 4, 'Python', 'Learning Python programming.', '2026-09-14 09:00:00');
INSERT INTO posts VALUES (5, 5, 'Databases', 'Databases are useful.', '2026-09-15 09:00:00');
INSERT INTO posts VALUES (6, 6, 'Visualization', 'Exploring data visualization.', '2026-09-16 09:00:00');
INSERT INTO posts VALUES (7, 7, 'Statistics', 'Learning about statistics.', '2026-09-17 09:00:00');
INSERT INTO posts VALUES (8, 8, 'Machine Learning', 'Introduction to machine learning.', '2026-09-18 09:00:00');
INSERT INTO posts VALUES (9, 9, 'SQL Queries', 'Practicing SQL queries.', '2026-09-19 09:00:00');
INSERT INTO posts VALUES (10, 10, 'Final Post', 'This is the final sample post.', '2026-09-20 09:00:00');
