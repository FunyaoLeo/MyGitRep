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
  <h2>Actor Information Page</h2>
  <?php
		if ($_SERVER["REQUEST_METHOD"] == "GET"){
			$identifier = $_GET["identifier"];
		}
		$query="select concat(first,\" \", last) as name, sex , dob, dod from Actor where id = $identifier;";
		$db = new mysqli('localhost','cs143','','CS143');
		if($db->connect_errno > 0){
			die('Unable to connect to database [' . $db->connect_error . ']');
		}
		if($identifier!=""){
			$rs = $db->query($query);
			echo "<h3>Actor Information is:</h3>";
			if($rs->num_rows>0){
				//find how many coloumns are there
				$field_cnt = $rs->field_count;
				echo "<table><tr>";		
				for($i = 0; $i<$field_cnt; $i++){
					$finfo = $rs->fetch_field_direct($i);
					echo "<th>".$finfo->name."</th>";
				}
				echo "</tr>";		
				while($row=$rs->fetch_row()){
					echo "<tr>";
					for($i = 0; $i<$field_cnt; $i++){
						if($row[$i]===null) $row[$i]="Still Alive";
						echo "<td>".$row[$i]."</td>";
					}
					echo "</tr>";
				}
				echo "</table>";	
			}
			echo "<h3>Actor's Movies and Role:</h3>";
			$query2="select MovieActor.mid, MovieActor.role, Movie.title from MovieActor, Movie, Actor where MovieActor.aid=Actor.id AND MovieActor.mid=Movie.id AND MovieActor.aid=$identifier ;";
			$rs2=$db->query($query2);
			if($rs2->num_rows>0){
				$field_cnt=$rs->field_count;
				echo "success";
				echo "<table><tr>";
				echo "<th>role</th>";
				echo "<th>movie title</rh>";
				echo "</tr>";
				while($row=$rs2->fetch_row()){
					echo "<tr>";
					echo "<td>".$row[1]."</td>";	
					echo "<td><a href = \" ShowMovie.php?identifier=".$row[0]."\">".$row[2]."</a></td>";
					echo "</tr>";
				}
				echo "</table>";
			}
			$rs->free();
			$rs2->free();
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







      