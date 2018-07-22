Usage:
Our project finishes all the criterian that are described in the project.
Four input pages:
Page I1: A page that lets users to add actor and/or director information. Here are some name examples: X.M.L Smith, J'son Lee, etc.
Page I2: A page that lets users to add movie information.
Some name examples: Beware the BLOB -- A Sequel, Willy Wonka and the Chocolate Factory
Page I3: A page that lets users to add comments to movies. i.e. This movie was terrible.
Page I4: A page that lets users to add "actor to movie" relation(s). i.e. Ryan Rosario stars in Alice in Wonderland (as the Madhatter, of
course!)
Page I5: A page that lets users to add "director to movie" relation(s). i.e. Johnny Depp directs Alice in Wonderland
Two browsing pages:
Page B1: A page that shows actor information.
Show links to the movies that the actor was in.
Page B2: A page that shows movie information.
Show Title, Producer, MPAA Rating, Director, Genre of this movie.
Show links to the actors/actresses that were in this movie.
Show the average score of the movie based on user feedbacks.
Show all user comments.
Contain "Add Comment" button which links to Page I3 where users can add comments.
One search page:
Page S1: A page that lets users search for an actor/actress/movie through a keyword search interface. (For actor/actress, you should
examine first/last name, and for movie, you should examine title.)
Your search page should support multi-word search, such as "Tom Hanks". For multi-word search, interpret space as "AND" relation.
That is, return all items that contain both words, "Tom" and "Hanks". Since the search page is for actor/actress/movie, so if there was a
movie named "I love Tom Hanks!", it should be returned. As for the output, you should sort them in a way that users could find an item
easily.

Additionally, we creat a fancy background and cool dropdown features for users to use. And we
add an additionally comment page for user to quick enter rather than have to comment through movie search page.

excute follow commands:
mysql TEST<create.sql
mysql TEST<load.sql
Then visit http://localhost:1438/~cs143/ and double click on navigation.php to use website.

Assignment:
Xuan Hu takes navigation and relation page
Fangyao Liu takes the rest.