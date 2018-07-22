#insert into Movie values (2, 'aaa', 1997, 5, 'Disney');
#violates Table Movie primary key constraint, '2' already #exists
#ERROR 1062 (23000) at line 1: Duplicate entry '2' for key #'PRIMARY'

#insert into Actor values (1, 'Leo', 'Fun', #'male','1995-01-01',null);
#violates Table Actor primary key constraint,'1'already exists
#ERROR 1062 (23000) at line 5: Duplicate entry '1' for key #'PRIMARY'

#insert into Director values (16, 'Xuan', #'Hu','1995-01-01',null);
#violates Table Director primary key constraint,'16'already #exists
#ERROR 1062 (23000) at line 9: Duplicate entry '16' for key #'PRIMARY'

#insert into MovieGenre (mid) values (100000) ;
#violates Table Movie foreign key(mid) constraint;'100000' #doesn't exist in Movie id
#ERROR 1452 (23000) at line 13: Cannot add or update a child #row: a foreign key constraint fails (`CS143`.`MovieGenre`, #CONSTRAINT `MovieGenre_ibfk_1` FOREIGN KEY (`mid`) REFERENCES #`Movie` (`id`))

#insert into MovieDirector (mid,did) values (100000,100000) ;
#violates Table Movie foreign key(mid) constraint ;'100000' #doesn't exist in Movie id
# ERROR 1452 (23000) at line 17: Cannot add or update a child #row: a foreign key constraint fails (`CS143`.`MovieDirector`, #CONSTRAINT `MovieDirector_ibfk_1` FOREIGN KEY (`mid`) #REFERENCES `Movie` (`id`))

#insert into MovieDirector (mid,did) values (4734,100000);
#violates Table Movie foreign key(did) constraint;'100000' #doesn't exist in Director id
#ERROR 1452 (23000) at line 21: Cannot add or update a child #row: a foreign key constraint fails (`CS143`.`MovieDirector`, #CONSTRAINT `MovieDirector_ibfk_2` FOREIGN KEY (`did`) #REFERENCES `Director` (`id`))

#insert into MovieActor(mid,aid) values (100000,100000);
#violates Table Movie foreign key(mid) constraint;'100000' #doesn't exist in Movie id
#ERROR 1452 (23000) at line 25: Cannot add or update a child #row: a foreign key constraint fails (`CS143`.`MovieActor`, #CONSTRAINT `MovieActor_ibfk_1` FOREIGN KEY (`mid`) REFERENCES #`Movie` (`id`))

#insert into MovieActor (mid,aid)values (4734,100000);
#violates Table Movie foreign key(aid) constraint;'100000' #doesn't exist in Actor id
# ERROR 1452 (23000) at line 29: Cannot add or update a child #row: a foreign key constraint fails (`CS143`.`MovieActor`, #CONSTRAINT `MovieActor_ibfk_2` FOREIGN KEY (`aid`) REFERENCES #`Actor` (`id`))

insert into Review (name,time,mid) values ("aaa","2017-07-23",100000);
#violates Table Movie foreign key(mid) constraint;'100000' #doesn't exist in Movie id
#cs143@cs143:~/www/project1b$ mysql CS143<violate.sql
#ERROR 1452 (23000) at line 33: Cannot add or update a child #row: a foreign key constraint fails (`CS143`.`Review`, #CONSTRAINT `Review_ibfk_1` FOREIGN KEY (`mid`) REFERENCES #`Movie` (`id`))

insert into Movie values (1, 'aaa', 1997, 6, 'Disney');
#violates Table Movie check constraint that rating is smaller than or equal to 5

insert into Actor values (1, 'Leo', 'Fun', 'male','1995-01-01','1993-01-01');
#violates Table Actor check constraint that dob should be smaller than dod

insert into Director values (16, 'Xuan', 'Hu','1995-01-01','1993-01-01');
#violates Table Director check constraint that dob should be smaller than dod
