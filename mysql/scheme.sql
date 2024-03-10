-- CREATE DATABASE playerdb;
-- USE playerdb;

DROP TABLE IF EXISTS player;

CREATE TABLE player (
  id INT AUTO_INCREMENT PRIMARY KEY,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  name VARCHAR(50) UNIQUE,
  team VARCHAR(100),
  goal INT
);

INSERT INTO player (name,team,goal)
VALUES ('sonny','spurs',10);

INSERT INTO player (name,team,goal)
VALUES ('kane','spurs',5);

INSERT INTO player (name,team,goal)
VALUES ('hyukjun','spurs',1);