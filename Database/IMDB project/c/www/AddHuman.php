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
          <li><a href="#">Add Actor/Director</a></li>
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
  <h2>Add new Actor/Director</h2>
  <form method="GET" action="#">
    <label class="radio-inline">
      <input type="radio" name="identity" value="Actor">Actor
    </label>
    <label class="radio-inline">
      <input type="radio" name="identity" value="Director">Director
    </label>
	<div>
	<div>
    <label class="radio-inline">
        <input type="radio" name="sex" value="Male">Male
    </label>
    <label class="radio-inline">
        <input type="radio" name="sex" value="Female">Female
    </label>
    <div class="form-group">
	<div class="col-xs-6">
      <label for="first_name">First Name</label>
      <input type="text" class="form-control" placeholder="Text input" name="fname">
	  <label for="last_name">Last Name</label>
      <input type="text" class="form-control" placeholder="Text input" name="lname">
      <label for="date_of_birth">Date of Birth</label>
      <input type="text" class="form-control" placeholder="Text input" name="dob">ie: 1995-05-10<br>
      <label for="date_of_die">Date of Death</label>
      <input type="text" class="form-control" placeholder="Text input" name="dod">(leave blank if alive now)<br>
      <button type="submit" class="btn btn-primary">Add</button>
	</div>
	</div>
  </form>
</div>

<?php
	if ($_SERVER["REQUEST_METHOD"] == "GET"){
		$identity = $_REQUEST['identity'];
		$sex = $_REQUEST['sex'];
		$fname = $_REQUEST['fname'];
		$lname = $_REQUEST['lname'];
		$dob = $_REQUEST['dob'];
		$dod = $_REQUEST['dod'];
	}
	
	
	//initiate an instance of databse
	$db = new mysqli('localhost','cs143','','CS143');
	if($db->connect_errno > 0){
		die('Unable to connect to database [' . $db->connect_error . ']');
	}
	//Get max ID number
	$query = "select id from MaxPersonID;";
	$rs = $db->query($query);
	$maxID = $rs->fetch_row()[0]+1;
	
	if($identity=="Actor"){
		if($dod!=""){
		    $query = "INSERT INTO Actor  VALUES(".$maxID.", \"".$lname."\", \"".$fname."\", \"".$sex."\", \"".$dob."\", \"".$dod."\");";
		}else{
		    $query = "INSERT INTO Actor (id, last, first, sex,dob) VALUES(".$maxID.", \"".$lname."\", \"".$fname."\", \"".$sex."\", \"".$dob."\");";
		}
		if($db->query($query)){
			$update="update MaxPersonID set id=id+1";
			$db->query($update);
			echo "Add successful!";
			echo "<div></div>";
			if($dod==""){
				echo "$identity : $fname $lname, $sex, born on $dob, alive now";
			}else{
				echo "$identity : $fname $lname, $sex, born on $dob, died on $dod";
	        }
		}
	}
	if($identity=="Director"){
		if($dod!=""){
		    $query = "INSERT INTO Director VALUES(".$maxID.", \"".$lname."\", \"".$fname."\", \"".$dob."\", \"".$dod."\");";
		}else{
		    $query = "INSERT INTO Director (id, last, first ,dob) VALUES(".$maxID.", \"".$lname."\", \"".$fname."\", \"".$dob."\");";
		}
		if($db->query($query)){
			$update="update MaxPersonID set id=id+1";
			$db->query($update);
			echo "Add successful!";
			echo "<div></div>";
			if($dod==""){
				echo "$identity : $fname $lname, born on $dob, alive now";
			}else{
				echo "$identity : $fname $lname, born on $dob, died on $dod";
			}
		}
	}
?>

</body>
</html>







      