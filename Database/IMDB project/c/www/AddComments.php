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

<?php
    if ($_SERVER["REQUEST_METHOD"] == "GET"){
		$identifier = $_GET['identifier'];
	}
	//initiate an instance of databse
	$db = new mysqli('localhost','cs143','','CS143');
	if($db->connect_errno > 0){
		die('Unable to connect to database [' . $db->connect_error . ']');
	}
	$queryMtitle = "select title from Movie order by title;";
	$Mtitle = $db->query($queryMtitle);
	if($identifier!=""){
	    $getmovie="select title from Movie where id=".$identifier.";";
		$selectmovie=$db->query($getmovie);
		$smovie=$selectmovie->fetch_row()[0];
	}
?>

<div class="container">
  <h2>Add Comments</h2>
  <form method="GET" action="#">
    <div class="form-group">
	<div class="col-xs-6">
	  <label for="reviewer">User name</label>
      <input type="text" class="form-control" placeholder="Text input" name="reviewer">
      <label for="movie">Movie:</label>
	    <select   class="form-control" name="movie" >
		    
	        <?php
			    echo "<option>".$smovie."</option>";
			    while($rowM=$Mtitle->fetch_assoc())
				    echo "<option value=\"".$rowM["title"]."\">".$rowM["title"]."</option>";
		    ?>
	  </select>
	  <label for="time">Rating</label>
        <select   class="form-control" name="rating" >
		  <option> </option>
		  <option>1</option>
		  <option>2</option>
		  <option>3</option>
		  <option>4</option>
		  <option>5</option>
	    </select>
	  <div>
	  <label for="comment">Comments:</label>
	  </div>
	  <textarea name="comments"  class="form-control" placeholder="Text input" rows="10" cols="40"></textarea><br>
  </form>
  <button type="submit" class="btn btn-primary" >Add Comments</button>
</div>

<?php
	if ($_SERVER["REQUEST_METHOD"] == "GET"){
		$reviewer = $_REQUEST['reviewer'];
		$movie=$_REQUEST['movie'];
		$rating=$_REQUEST['rating'];
		$comments=$_REQUEST['comments'];
	}
    
	$queryMid = "select id from Movie where title=\"" .$movie."\";";
	$rsM = $db->query($queryMid);
	$Mid = $rsM->fetch_row()[0];
	$query = "INSERT INTO Review VALUES(\"".$reviewer."\",now(), ".$Mid.", ".$rating.",\"".$comments."\");";
	$db->query($query);
	
?>

</body>
</html>
