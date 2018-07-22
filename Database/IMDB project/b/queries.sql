#find the actors of movie "Die another day"
select concat(first ," ", last) as name 
from   Actor,Movie,MovieActor
where  Movie.title='Die Another Day' 
AND Movie.id=MovieActor.mid 
AND MovieActor.aid=Actor.id;

#number of actors that showed up in multiple movies
select count(larger) as num
from(select count(aid) as larger
    from MovieActor
    group by aid
    having count(aid)>2) as transformed;

#find the lastname and the first name of actor who appear in movies #most times
select Actor.id,Actor.first,Actor.last,count(Movie.id)as showtime
from   Actor,Movie,MovieActor
where  Movie.id=MovieActor.mid 
AND MovieActor.aid=Actor.id
group by Actor.id
order by count(Movie.id) DESC
limit 1;

