<!DOCTYPE html>
<html>
<body>

<?php
echo "<h2>Calculator</h2>";
echo "(project 1a by Fangyao Liu & Xuan Hu)<br>";
echo "Type an expression in the following box (e.g., 10.5+20*3/25)."
?> 

<form method="get" action="<?php echo $_SERVER['PHP_SELF'];?>">
  <input type="text" name="expression">
  <input type="submit" value="Calculate">
</form>

<?php
echo "<ul>";
echo "<li>Only numbers and +,-,* and / operators are allowed in the expression.  </li>";
echo "<li>The evaluation follows the standard operator precedence.  </li>";
echo "<li>The calculator does not support parentheses.  </li>";
echo "<li>The calculator handles invalid input \"gracefully\". It does not output PHP error messages.  </li>";
echo "</ul>";

echo "Here are some(but not limit to) reasonable test cases:<br>";
echo "<ol type='1'>";
echo "<li>A basic arithmetic operation: 3+4*5=23  </li>";
echo "<li>An expression with floating point or negative sign : -3.2+2*4-1/3 = 4.46666666667, 3*-2.1*2 = -12.6  </li>";
echo "<li>Some typos inside operation (e.g. alphabetic letter): Invalid input expression 2d4+1  </li>";
echo "</ol>";

echo "<h2>Result</h2>";

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // collect value of input field
    $expression = $_REQUEST['expression'];
    if(empty($expression))
		;
	else{
		$expression = preg_replace('/\s+/', '', $expression);
		if(is_numeric($expression[0])||($expression[0]==="-"&&is_numeric($expression[1]))){
			$pattern = "/^([\+\-\*\/]?\-?(?!0+\d+)\d+(\.\d+)?)+$/";
			$division0 = "/\/(0($|[\+\-\*\/]))|(0\.0+($|[\+\-\*\/]))/";
			if(preg_match($pattern, $expression)){
				if(preg_match($division0, $expression))
					echo "Division by zero error!<br>";
				else{
					$result = eval("return $expression;");
					echo $expression . " = " . $result;
				}
			}
			else
				echo "Invalid Expression!<br>";
		}
		else
			echo "Invalid Expression!<br>";
	}
}

?>


</body>
</html>