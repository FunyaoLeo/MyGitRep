<!DOCTYPE html>
<html lang="en">
<head>
  <title>Movie & Actor DB System</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <style>
  h3 {
	  font-weight: 300;
	  color: #FFFFFF;
  }
  .jumbotron {
      background-color: #0059b3;
      color: #fff;
      padding: 70px 25px;
      font-family: Montserrat, sans-serif;
  }.bg {
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

<div class="jumbotron text-center">
  <h1>Movie & Actor DB System</h1>
  <p>Designed by Fangyao Liu and Xuan Hu</p> 
</div>

<div class="container">

  <div class="row">
  <div class="bg"></div>
    <div class="col-sm-4">
		<h3>Add New Content</h3>
		<div class="dropdown">
		<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Input Option
		<span class="caret"></span></button>
		<ul class="dropdown-menu">
		<li><a href="AddHuman.php">Add Actor/Director</a></li>
		<li><a href="AddMovie.php">Add Movie Information</a></li>
		<li><a href="AddComments.php">Add Comments</a></li>
		<li><a href="MovieActor.php">Add Movie/Actor Relation</a></li>
		<li><a href="MovieDirector.php">Add Movie/Director Relation</a></li>
		</ul>
		</div> 
    </div>
    <div class="col-sm-4">
		<h3>Browse Content</h3>
		<div class="dropdown">
		<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Browse Option
		<span class="caret"></span></button>
		<ul class="dropdown-menu">
		<li><a href="ShowActor.php">Show Actor Information</a></li>
		<li><a href="ShowMovie.php">Show Movie Information</a></li>
		</ul>
		</div> 
    </div>
    <div class="col-sm-4">
		<h3>Search Content</h3>
		<div class="dropdown">
		<button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Search Option
		<span class="caret"></span></button>
		<ul class="dropdown-menu">
		<li><a href="Search.php">Search Actor/Actress/Movie</a></li>
		</ul>
		</div> 
    </div>
  </div>
</div>


</body>
</html>
