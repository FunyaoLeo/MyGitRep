-- select database
USE CS144;

-- drop existing tables
DROP TABLE IF EXISTS Posts;

-- create table Posts
CREATE TABLE Posts(
  username	VARCHAR(40),
  postid	INTEGER,
  title		VARCHAR(100),
  body		TEXT,
  modified	TIMESTAMP DEFAULT '2000-01-01 00:00:00',
  created	TIMESTAMP DEFAULT '2000-01-01 00:00:00',
  PRIMARY KEY(username, postid)
);
