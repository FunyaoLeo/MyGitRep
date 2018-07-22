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
  <h2>Searching Pages:</h2>
  <form method="GET" action="#">
    <div class="form-group">
	<div class="col-xs-6">
      <label for="title">Search:</label>
      <input type="text" class="form-control" placeholder="Text input" name="text">
  </form>
  <button type="submit" class="btn btn-primary" style="position:relative; top: 10px;">Click me!</button>
  <br>
  <br>
  <br>
  
<?php
	if ($_SERVER["REQUEST_METHOD"] == "GET"){
		$text = $_REQUEST['text'];
	}
	$db = new mysqli('localhost','cs143','','CS143');
	if($db->connect_errno > 0){
		die('Unable to connect to database [' . $db->connect_error . ']');
	}
	$names = explode(" ", $text);
	$names_size = count($names);
	

	$queryActor = "select id, first, last, dob from Actor where first like ";
	$queryMovie = "select id, title, year from Movie where title like \"";
	
	if($names_size>2){
		for($x=0; $x<$names_size; $x++){
			$queryMovie = $queryMovie."%".$names[$x];
		}
		$queryMovie = $queryMovie."%\";";
		echo "<h2>Matching Movie are:</h2>";
		
		$rs = $db->query($queryMovie);
		if($rs->num_rows>0){
			//find how many coloumns are there
			$field_cnt = $rs->field_count;
			echo "<table><tr>";
			for($i = 1; $i<$field_cnt; $i++){
				$finfo = $rs->fetch_field_direct($i);
				echo "<th>".$finfo->name."</th>";
			}
			echo "</tr>";
			
			while($row=$rs->fetch_row()){
				echo "<tr>";
				for($i = 1; $i<$field_cnt; $i++){
					if($row[$i]===null) $row[$i]="N/A";
					echo "<td><a href = \" ShowMovie.php?identifier=".$row[0]."\">".$row[$i]."</a></td>";
				}
				echo "</tr>";
			}
			echo "</table>";
			
				$rs->free();
		}
	}
	
	elseif($names_size==2){
		$queryActor = $queryActor."\"%".$names[0]."%\" and last like \"%".$names[1]."%\";";
		echo "<h2>Matching Actors are:</h2>";
		
		$rs = $db->query($queryActor);
		if($rs->num_rows>0){
			//find how many coloumns are there
			echo "<table><tr>";
			for($i = 0; $i<2; $i++){
				if($i==0)
					echo "<th> Name </th>";
				else
					echo "<th> Date of Birth </th>";
			}
			echo "</tr>";
			
			while($row=$rs->fetch_row()){
				echo "<tr>";
				echo "<td><a href = \" ShowActor.php?identifier=".$row[0]."\">".$row[1]." ".$row[2]."</a></td>";
				echo "<td><a href = \" ShowActor.php?identifier=".$row[0]."\">".$row[3]."</a></td>";
				echo "</tr>";
			}
			echo "</table>";
			
				$rs->free();
		}
		
		for($x=0; $x<$names_size; $x++){
			$queryMovie = $queryMovie."%".$names[$x];
		}
		$queryMovie = $queryMovie."%\";";
		echo "<h2>Matching Movie are:</h2>";
		
		$rs = $db->query($queryMovie);
		if($rs->num_rows>0){
			//find how many coloumns are there
			$field_cnt = $rs->field_count;
			echo "<table><tr>";
			for($i = 1; $i<$field_cnt; $i++){
				$finfo = $rs->fetch_field_direct($i);
				echo "<th>".$finfo->name."</th>";
			}
			echo "</tr>";
			
			while($row=$rs->fetch_row()){
				echo "<tr>";
				for($i = 1; $i<$field_cnt; $i++){
					if($row[$i]===null) $row[$i]="N/A";
					echo "<td><a href = \" ShowMovie.php?identifier=".$row[0]."\">".$row[$i]."</a></td>";

				}
				echo "</tr>";
			}
			echo "</table>";
			
				$rs->free();
		}
	}
	elseif($names_size==1 and $names[0]!=""){
		$queryActor = $queryActor."\"%".$names[0]."%\" or last like \"%".$names[0]."%\";";
		echo "<h2>Matching Actors are:</h2>";
		
		$rs = $db->query($queryActor);
		if($rs->num_rows>0){
			//find how many coloumns are there
			$field_cnt = $rs->field_count;
			echo "<table><tr>";
			for($i = 0; $i<2; $i++){
				if($i==0)
					echo "<th> Name </th>";
				else
					echo "<th> Date of Birth </th>";
			}
			echo "</tr>";
			
			while($row=$rs->fetch_row()){
				echo "<tr>";
				echo "<td><a href = \" ShowActor.php?identifier=".$row[0]."\">".$row[1]." ".$row[2]."</a></td>";
				echo "<td><a href = \" ShowActor.php?identifier=".$row[0]."\">".$row[3]."</a></td>";
				echo "</tr>";
			}
			echo "</table>";
			
				$rs->free();
		}
		
		for($x=0; $x<$names_size; $x++){
			$queryMovie = $queryMovie."%".$names[$x];
		}
		$queryMovie = $queryMovie."%\";";
		echo "<h2>Matching Movie are:</h2>";
		
		$rs = $db->query($queryMovie);
		if($rs->num_rows>0){
			//find how many coloumns are there
			$field_cnt = $rs->field_count;
			echo "<table><tr>";
			for($i = 1; $i<$field_cnt; $i++){
				$finfo = $rs->fetch_field_direct($i);
				echo "<th>".$finfo->name."</th>";
			}
			echo "</tr>";
			
			while($row=$rs->fetch_row()){
				echo "<tr>";
				for($i = 1; $i<$field_cnt; $i++){
					if($row[$i]===null) $row[$i]="N/A";
					echo "<td><a href = \" ShowMovie.php?identifier=".$row[0]."\">".$row[$i]."</a></td>";
				}
				echo "</tr>";
			}
			echo "</table>";
			
				$rs->free();
		}
	}
	
	$db->close();
?>
</div>




</body>
</html>

