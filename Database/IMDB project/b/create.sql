CREATE TABLE Movie(
id                           INT,
title                       VARCHAR(100),
year                      INT,
rating                   VARCHAR(10),
company             VARCHAR(50),
primary key (id),
CHECK (rating>=0 and rating <=5)
)ENGINE=INNODB;
#Table Movie cannot have tuples of same id
#the rating should be between 0 and 5 

CREATE TABLE Actor(
id                           INT,
last                        VARCHAR(20),
first                       VARCHAR(20),
sec                        VARCHAR(6),
dob                       DATE,
dod                       DATE,
primary key (id),
CHECK(dob<dod)
)ENGINE=INNODB;
#Table Actor cannot have tuples of same id
#dob has to be smaller than dod

CREATE TABLE Director(
id                           INT,
last                        VARCHAR(20),
first                       VARCHAR(20),
dob                       DATE,
dod                       DATE,
primary key (id),
CHECK(dob<dod)
)ENGINE=INNODB;
#Table Director cannot have tuples of same id
#dob has to be smaller than dod

CREATE TABLE MovieGenre(
mid                          INT,
genre                      VARCHAR(20),
primary key (mid),
foreign key (mid) references Movie(id)
)ENGINE=INNODB;
#Table MovieGenre cannot contain mid that is not in Movie Table

CREATE TABLE MovieDirector(
mid                         INT,
did                          INT,
primary key (mid,did),
foreign key (mid) references Movie(id),
foreign key (did) references Director(id)
)ENGINE=INNODB;
#Table MovieDirector cannot contain mid that is not in Movie Table
#Table MovieDirector cannot contain did that is not in Director Table

CREATE TABLE MovieActor(
mid                         INT,
aid                           INT,
role                         VARCHAR(50),
primary key (mid,aid),
foreign key (mid) references Movie(id),
foreign key (aid) references Actor(id)
)ENGINE=INNODB;
#Table MovieActor cannot contain mid that is not in Movie Table
#Table MovieActor cannot contain aid that is not in Actor Table

CREATE TABLE Review(
name                       VARCHAR(20),
time                         TIMESTAMP,
mid                           INT,
rating                        INT,
comment                 VARCHAR(500),
primary key (name, time),
foreign key (mid) references Movie(id)
)ENGINE=INNODB;
#Table Review cannot contain mid that is not in Movie Table

CREATE TABLE MaxPersonID(
id                                INT,
primary key (id)
)ENGINE=INNODB;

CREATE TABLE MaxMovieID(
id                                INT,
primary key (id)
)ENGINE=INNODB;
