<?php
	
	
	// variables
	$start_date = $stop_date = "";
	
	$servername = "128.153.22.104";
	$username = "historicalquery";
	$password = "ClarksonUser";
	$table_name = "inverter_and_weather_data";
	$db_name = "blackboard_gui";
	
	$query_building = "SELECT ";
	
	$query_requested_fields = "";
	
	if($_SERVER["REQUEST_METHOD"] = "POST") {
		$start_date = date('Y-m-d H:i', strtotime($_POST['start-date']));
		$stop_date = date('Y-m-d H:i', strtotime($_POST['end-date']));
		
		$query_requested_fields_arr = get_query_from();
		$query_requested_fields = implode(", ", $query_requested_fields_arr);
		
		$query_building .= $query_requested_fields . " FROM " . $table_name;
		
		$query_building .= " WHERE time_stamp BETWEEN CAST('" . $start_date . ":00' AS DATETIME) AND CAST('" . $stop_date . ":00' AS DATETIME);";
		
		$file_name = $start_date . "_to_" . $stop_date . ".csv";
		
		// Create connection
		$conn = new mysqli($servername, $username, $password, $db_name);

		// Check connection
		if ($conn->connect_error) {
			//die("Connection failed: " . $conn->connect_error);
		} 
		
		$result = $conn->query($query_building);
		
		if (!$result) {
			//trigger_error('Invalid Query: ' . $conn->error);
		} else {
			// create CSV file
			header("Content-Type: text/csv");
			header("Content-Disposition: attatchment; filename=${file_name}");
			
			$output = fopen('php://output', 'wb');
			
			// column headings
			fputcsv($output, $query_requested_fields_arr);
			
			
			
			// insert rows into csv
			while($row = $result->fetch_assoc()) {
				fputcsv($output, $row);
			}
			
			fclose($output);
		}
		
		$conn->close();
		exit;
		
		/*
		if (($result->num_rows) > 0) {
			// output data of each row
			while($row = $result->fetch_assoc()) {
				echo $result->fetch_row() . "<br>";
			} 	
		} else {
			echo "0 results";
		}
		$conn->close();
		*/
		

	}
	
?>


<?php

function get_query_from() {
	$from_array = array();
	$query_from = "";
	
	if(isset($_POST['time_stamp']) && $_POST['time_stamp']){
			array_push($from_array, "time_stamp");
		}
	
	if(isset($_POST['vdc1']) && $_POST['vdc1'])
	{
		array_push($from_array, "VDC1");
	}
	
	if(isset($_POST['idc1']) && $_POST['idc1'])
	{
		array_push($from_array, "IDC1");
	}
	
	if(isset($_POST['pdc1']) && $_POST['pdc1'])
	{
		array_push($from_array, "PDC1");
	}
	
	if(isset($_POST['vdc2']) && $_POST['vdc2'])
	{
		array_push($from_array, "VDC2");
	}
	
	if(isset($_POST['idc2']) && $_POST['idc2'])
	{
		array_push($from_array, "IDC2");
	}
	
	if(isset($_POST['pdc2']) && $_POST['pdc2'])
	{
		array_push($from_array, "PDC2");
	}
	
	if(isset($_POST['vac']) && $_POST['vac'])
	{
		array_push($from_array, "VAC");
	}
	
	if(isset($_POST['iac']) && $_POST['iac'])
	{
		array_push($from_array, "IAC");
	}
	
	if(isset($_POST['pac']) && $_POST['pac'])
	{
		array_push($from_array, "PAC");
	}
	
	if(isset($_POST['tinv']) && $_POST['tinv'])
	{
		array_push($from_array, "tinv");
	}
	
	if(isset($_POST['tint']) && $_POST['tint'])
	{
		array_push($from_array, "TINT");
	}
	
	if(isset($_POST['energy']) && $_POST['energy'])
	{
		array_push($from_array, "ENERGY");
	}
	
	if(isset($_POST['riso']) && $_POST['riso'])
	{
		array_push($from_array, "RISO");
	}
	
	if(isset($_POST['ileak']) && $_POST['ileak'])
	{
		array_push($from_array, "ILEAK");
	}
	
	if(isset($_POST['genfreq']) && $_POST['genfreq'])
	{
		array_push($from_array, "GENFREQ");
	}
	
	if(isset($_POST['temp']) && $_POST['temp'])
	{
		array_push($from_array, "temp_celsius");
	}
	
	if(isset($_POST['relative-humidity']) && $_POST['relative-humidity'])
	{
		array_push($from_array, "relative_humidity");
	}
	
	if(isset($_POST['dewpoint']) && $_POST['dewpoint'])
	{
		array_push($from_array, "dewpoint_celsius");
	}
	
	
	if(isset($_POST['wind-heading']) && $_POST['wind-heading'])
	{
		array_push($from_array, "wind_heading");
	}
	
	
	if(isset($_POST['wind-speed']) && $_POST['wind-speed'])
	{
		array_push($from_array, "windspeed_mph");
	}	
	
	if(isset($_POST['pressure']) && $_POST['pressure'])
	{
		array_push($from_array, "pressure_mb");
	}
	
	return $from_array;
	
	
}
?>