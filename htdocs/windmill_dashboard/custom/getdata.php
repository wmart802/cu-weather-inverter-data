<?php
//setting header to json
header('Content-Type: application/json');

//database
define('DB_HOST', '128.153.22.104');
define('DB_USERNAME', 'pythondev');
define('DB_PASSWORD', 'WMDccp2018!');
define('DB_NAME', 'blackboard_gui');

date_default_timezone_set('America/New_York');

$oneDayAgo = strtotime("-1 days");

$formattedOneDayAgo = date('Y-m-d H:i:s',$oneDayAgo);
//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}


//query to get data from the table
$query = sprintf("SELECT time_stamp, PAC FROM inverter_and_weather_data WHERE time_stamp >= '" . $formattedOneDayAgo . "'");
//$query = sprintf("SELECT * FROM inverter_and_weather_data");
//execute query
$result = $mysqli->query($query);

$data = array();

//loop through the returned data

	while($row = $result->fetch_assoc()) {
		$data[] = $row;
	}
	
	//free memory associated with result
	$result->close();




//close connection
$mysqli->close();

//now print the data
print json_encode($data);
?>