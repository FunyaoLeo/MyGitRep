<!DOCTYPE html>
<html lang="en">
<head>
  <title>Add Actor/Director</title>
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
	  <li><a href="#">Add Movie/Actor Relation</a></li>
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

<?php
	//initiate an instance of databse
	$db = new mysqli('localhost','cs143','','CS143');
	if($db->connect_errno > 0){
		die('Unable to connect to database [' . $db->connect_error . ']');
	}
	$queryMtitle = "select title from Movie order by title;";
	$Mtitle = $db->query($queryMtitle);
	$queryActor = "select first,last from Actor order by first, last;";
	$Actor = $db->query($queryActor);
?>

<div class="container">
  <h2>Add new Actor Movie Relation</h2>
  <form method="GET" action="#">
    <div class="form-group">
	<div class="col-xs-10">
      <label for="movie_title">Movie Title</label>
      <select   class="form-control" name="title">
	  <option> </option>
	  <?php
			while($rowM=$Mtitle->fetch_assoc())
				echo "<option value=\"".$rowM["title"]."\">".$rowM["title"]."</option>";
			
	  ?>
	  </select>
	  <label for="actor">Actor</label>
      <select   class="form-control" name="actor">
	  <option> </option>
	  <?php
			while($rowA=$Actor->fetch_assoc())
				echo "<option value=\"".$rowA["first"]." ".$rowA["last"]."\">".$rowA["first"]." ".$rowA["last"]."</option>";
	  ?>
	  </select>
	  <label for="Role">Role:</label>
      <input type="text" class="form-control" placeholder="Text input" name="role"><br>
      <button type="submit" class="btn btn-primary">Add</button>
	</div>
	</div>
  </form>
</div>

<?php
	if ($_SERVER["REQUEST_METHOD"] == "GET"){
		$title = $_REQUEST['title'];
		$actor = $_REQUEST['actor'];
		$role = $_REQUEST['role'];
	}

	$queryMid = "select id from Movie where title=\"" .$title."\";";
	$rsM = $db->query($queryMid);
	$Mid = $rsM->fetch_row()[0];
	
	$names = explode(" ", $actor);
	$queryAid = "select id from Actor where first=\"" .$names[0]."\" and last=\"" .$names[1]."\";";
	$rsA = $db->query($queryAid);
	$Aid = $rsA->fetch_row()[0];
	
	$query = "INSERT INTO MovieActor VALUES(".$Mid.", ".$Aid.", \"".$role."\");";
	$db->query($query);
	
	$Mtitle->free();
	$Actor->free();
	$rsM->free();
	$rsA->free();
?>

</body>
</html>







      