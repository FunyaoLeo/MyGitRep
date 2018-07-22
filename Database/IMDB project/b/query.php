<!DOCTYPE html>
<html>
<body>
<style>
table, th, td {
    border: 1px solid black;
}
</style>

<?php
echo "<h2>Query Interface</h2>";
echo "(project 1b by Fangyao Liu & Xuan Hu)<br>";
echo "Type a query expression in the following text area<br> ";
echo "e.g. SELECT * FROM Actor WHERE id=10;<br>";
?> 


<form method="get" action="<?php echo $_SERVER['PHP_SELF'];?>">
  <textarea name="query" rows="10" cols="40"></textarea><br>
  <input type="submit" value="search">
</form>

<?php

echo "<h2>Result</h2>";

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // collect value of input field
    $query = $_REQUEST['query'];
	
	//initiate an instance of databse
	$db = new mysqli('localhost','cs143','','CS143');
	if($db->connect_errno > 0){
		die('Unable to connect to database [' . $db->connect_error . ']');
	}
	
	$rs = $db->query($query);
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
				if($row[$i]===null) $row[$i]="N/A";
				echo "<td>".$row[$i]."</td>";
			}
			echo "</tr>";
		}
		echo "</table>";
		
			$rs->free();
	}
}

?>


</body>
</html>