<!DOCTYPE html>
<html lang="en">
<head>
  <title>ShowMovie</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>  
  <style>
  .navbar {
      margin-bottom: 0;
      background-color: #0059B3;
      z-index: 9999;
      border: 0;
      font-size: 15px !important;
      line-height: 1.42857143 !important;
      letter-spacing: 4px;
      border-radius: 0;
      font-family: Montserrat, sans-serif;
  }
  .navbar-nav li a:hover, .navbar-nav li.active a {
      color: #0059B3 !important;
      background-color: #fff !important;
  }
  .navbar-default .navbar-toggle {
      border-color: #0059B3;
      color: #fff !important;
  }
  .bg {
	position: absolute;
	z-index: -1;
	top: 0;
	bottom: 0;
	left: 0;
	right: 0;
	background: url(Navibackground.png) center center;
	opacity: 0.75;
        width: 100%;
        height: 100%;
  }
  table, th, td {
    border: 1px solid black;
  }
  </style>
  </head>
<body>


<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <ul class="nav navbar-nav">
      <li ><a href="navigation.php">Home</a></li>
      <li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">Add<span class="caret"></span></a>
        <ul class="dropdown-menu">
          <li><a href="AddHuman.php">Add Actor/Director</a></li>
	  <li><a href="AddMovie.php">Add Movie Information</a></li>
	  <li><a href="AddComments.php">Add Comments</a></li>
	  <li><a href="MovieActor.php">Add Movie/Actor Relation</a></li>
          <li><a href="MovieDirector.php">Add Movie/Director Relation</a></li>
        </ul>
      </li>
      <li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">Show<span class="caret"></span></a>
        <ul class="dropdown-menu">
          <li><a href="ShowActor.php">Show Actor Information</a></li>
	  <li><a href="ShowMovie.php">Show Movie Information</a></li>
        </ul>
      </li>
      <li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">Search<span class="caret"></span></a>
        <ul class="dropdown-menu">
          <li><a href="Search.php">Search Actor/Actress/Movie</a></li>
        </ul>
      </li>
    </ul>
  </div>
</nav>


<div class="container">
  <h2>Movie Information Page</h2>
  <?php
    //initiate an instance of databse
	$db = new mysqli('localhost','cs143','','CS143');
	if($db->connect_errno > 0){
		die('Unable to connect to database [' . $db->connect_error . ']');
	}
	
	if ($_SERVER["REQUEST_METHOD"] == "GET"){
		$identifier = $_GET["identifier"];
	}
	if($identifier!=""){
		$mquery = "select * from Movie where id=".$identifier.";";
		$rsM = $db->query($mquery);
		$Movie = $rsM->fetch_assoc();
		

		$dquery = "select first, last from Director, MovieDirector where Director.id=MovieDirector.did and MovieDirector.mid=".$identifier.";";
		$rsMd = $db->query($dquery);
		$director = $rsMd->fetch_assoc();
		
		$genre_query = "select genre from MovieGenre where mid=".$identifier.";";
		$rsMg = $db->query($genre_query);
		
		echo "<h3>Movie Information is:</h3>";
		echo "Title: ".$Movie["title"]."(".$Movie["year"].")<br>";
		echo "Producer: ".$Movie["company"]."<br>";
		echo "MPAA rating: ".$Movie["rating"]."<br>";
		echo "Director: ".$director["first"]." ".$director["last"]."<br>";
		echo "Genre: ";
		$genre=$rsMg->fetch_assoc();
		echo $genre["genre"];
		while($genre=$rsMg->fetch_assoc()){
			echo ", ".$genre["genre"];
		}
		echo "<br><h3>Actors in this movie:</h3>";
		$queryActor = "select id, first, last, role from Actor, MovieActor where Actor.id = MovieActor.aid and MovieActor.mid=".$identifier.";";
		$rsA = $db->query($queryActor);
		if($rsA->num_rows>0){
			//find how many coloumns are there
			echo "<table><tr>";
			for($i = 0; $i<2; $i++){
				if($i==0)
					echo "<th> Name </th>";
				else
					echo "<th> Role </th>";
			}
			echo "</tr>";
			
			while($row=$rsA->fetch_row()){
				echo "<tr>";
				echo "<td><a href = \" ShowActor.php?identifier=".$row[0]."\">".$row[1]." ".$row[2]."</a></td>";
				echo "<td><a href = \" ShowActor.php?identifier=".$row[0]."\">".$row[3]."</a></td>";
				echo "</tr>";
			}
			echo "</table>";
			
				$rsA->free();
		}
		echo "<h3>User Review:</h3>";
		echo "<a href = \" AddComments.php?identifier=".$identifier."\">Give a review</a><br>";
		
		$query1="select AVG(rating) from Review where mid=$identifier;";
		$reB=$db->query($query1);
		$row=$reB->fetch_row();
		$avgrat=$row[0];
		if($avgrat!=""){
			echo "Average rating:  ";
			echo "$avgrat <br>";
			$query2="select name,time, rating,comment from Review where mid=$identifier ;";
			$reC=$db->query($query2);
			
			echo "<table><tr>";
            echo "<th>User name</th>";
			echo "<th>Time</th>";
			echo "<th>Rating</th>";
			echo "<th>Comment</th>";
			echo "</tr>";		
			while($row=$reC->fetch_row()){
				echo "<tr>";
				for($i = 0; $i<4; $i++){
					echo "<td>".$row[$i]."</td>";
				}
				echo "</tr>";
			}
			echo "</table>";
		}
		
	}

  ?>
  <form method="GET" action="Search.php">
    <div class="form-group">
	<div class="col-xs-6">
      <label for="title">Search:</label>
      <input type="text" class="form-control" placeholder="Text input" name="text">
  </form>
  <button type="submit" class="btn btn-primary" style="position:relative; top: 10px;">Search</button>
</div>


</body>
</html>









      