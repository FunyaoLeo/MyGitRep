<!DOCTYPE html>
<html lang="en">
<head>
  <title>Add New Movie</title>
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
  </style>
  </head>
<body>

<div class="bg"></div>
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
  <h2>Add New Movie</h2>
  <form method="GET" action="#">
    <div class="form-group">
	<div class="col-xs-6">
      <label for="title">Title:</label>
      <input type="text" class="form-control" placeholder="Text input" name="title">
	  <label for="company">Company:</label>
      <input type="text" class="form-control" placeholder="Text input" name="company">
      <label for="year">Year:</label>
      <input type="text" class="form-control" placeholder="Text input" name="year">ie: 1984<br>
      <label for="MPAA_Rating">MPAA Rating:</label>
	  <select   class="form-control" name="rate">
                        <option value="G">G</option>
                        <option value="NC-17">NC-17</option>
                        <option value="PG">PG</option>
                        <option value="PG-13">PG-13</option>
                        <option value="R">R</option>
                        <option value="surrendere">surrendere</option>
       </select>
	  <label for="genre">Genre:</label>
	  <label class="checkbox-inline">
	  <input type="checkbox" name="genre[]" value="Action">Action
	  </label>
	  <label class="checkbox-inline" >
      <input type="checkbox" name="genre[]" value="Adult">Adult
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Adventure">Adventure
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Animation">Animation
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Comedy">Comedy
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Crime">Crime
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Documentary">Documentary
	  </label>
	  <label class="radio-inline">
      <input type="checkbox" name="genre[]" value="Drama">Drama
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Family">Family
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Fantasy">Fantasy
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Horror">Horror
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Musical">Musical
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Mystery">Mystery
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Romance">Romance
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Sci-Fi">Sci-Fi
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Short">Short
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Thriller">Thriller
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="War">War
	  </label>
	  <label class="checkbox-inline">
      <input type="checkbox" name="genre[]" value="Western">Western
	  </label>
  </form>
  <button type="submit" class="btn btn-primary" style="position:relative; top: 10px;">ADD</button>
</div>

<?php
    if ($_SERVER["REQUEST_METHOD"] == "GET"){
		$title = $_REQUEST['title'];
		$company = $_REQUEST['company'];
		$year = $_REQUEST['year'];
		$rate = $_REQUEST['rate'];
		$genre = $_REQUEST['genre'];
	}
	

	//initiate an instance of databse
	$db = new mysqli('localhost','cs143','','CS143');
	if($db->connect_errno > 0){
		die('Unable to connect to database [' . $db->connect_error . ']');
	}
	//Get max ID number
	$query = "select id from MaxMovieID;";
	$rs = $db->query($query);
	$maxID = $rs->fetch_row()[0]+1;
	$query = "INSERT INTO Movie VALUES(".$maxID.", \"".$title."\", ".$year.", \"".$rate."\", \"".$company."\");";
	if($db->query($query)){			
		$update="update MaxMovieID set id=id+1";
		$db->query($update);
		foreach($genre as $g){
		    $insertgenre="insert into MovieGenre values(".$maxID.",\"".$g."\");";
		    $db->query($insertgenre);
		}
		echo "Add success!";
	}
	
?>

</body>
</html>







      