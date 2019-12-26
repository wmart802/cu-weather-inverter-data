<!DOCTYPE HTML>  
<html>
	<head>
		<style>
			.error {color: #FF0000;}
		</style>
		<link href="historical-query-style.css" rel="stylesheet">
	</head>
	<body> 
		<h1>
			Clarkson Historical TAC Turbine Data Query
		</h1>
		<h3>
			This page allows you to select a date range and values to download from the database. The data will be downloaded in CSV format.
		</h3>
		</br>
		<p>Select the dates and data fields you would like to download.</p>
		<form action="lib/inputProcessing.php" method="post">
			<section>
				<h4>Date Range</h4>
				<ul style="width: 290px;">
					<li>
						<label for="start-date">Start Date:</label>
						<input type="datetime-local" id="start-date"
							name="start-date" value="2019-04-17T00:00"
						min="2019-04-17T00:00" max="2020-01-01T00:00">
					</li>
					<br>
					<li>
						<label for="end-time">End Date:&nbsp;</label>
						<input type="datetime-local" id="end-date"
							name="end-date" value="2018-06-12T19:30"
						min="2018-04-11T00:00" max="2020-01-01T00:00">
					</li>
				</ul>
			</section>
			<section>

				<fieldset>
					<legend>
						<h4>Data Fields</h4>
					</legend>
					<!--<div>
						<label for="check-all">Select All</label>
						<input type="checkbox" id="check-all"
						name="check-all" value=1>
						
						<label for="check-none">Select None</label>
						<input type="checkbox" id="check-none"
						name="check-none">
					</div> -->
					<br>
					<ul>
						<li>
							<label for="time_stamp">time_stamp</label>
							<input type="checkbox" id="time_stamp"
							name="time_stamp"/>
						</li>
						<li>
							<label for="vdc1">VDC1</label>
							<input type="checkbox" id="vdc1"
							name="vdc1">
						</li>
						<li>
							<label for="idc1">IDC1</label>
							<input type="checkbox" id="idc1"
							name="idc1">
						</li>
						<li>
							<label for="pdc1">PDC1</label>
							<input type="checkbox" id="pdc1"
							name="pdc1">
						</li>
						<li>
							<label for="vdc2">VDC2</label>
							<input type="checkbox" id="vdc2"
							name="vdc2">
						</li>
						<li>
							<label for="idc2">IDC2</label>
							<input type="checkbox" id="idc2"
							name="idc2">
						</li>
						<li>
							<label for="pdc2">PDC2</label>
							<input type="checkbox" id="pdc2"
							name="pdc2">
						</li>
						<li>
							<label for="vac">VAC</label>
							<input type="checkbox" id="VAC"
							name="VAC">
						</li>
						<li>
							<label for="iac">IAC</label>
							<input type="checkbox" id="iac"
							name="iac">
						</li>
						<li>
							<label for="pac">PAC</label>
							<input type="checkbox" id="pac"
							name="pac">
						</li>
						<li>
							<label for="tinv">TINV</label>
							<input type="checkbox" id="tinv"
							name="tinv">
						</li>
						<li>
							<label for="tint">TINT</label>
							<input type="checkbox" id="TINT"
							name="TINT">
						</li>
						<li>
							<label for="energy">ENERGY</label>
							<input type="checkbox" id="energy"
							name="energy">
						</li>
						<li>
							<label for="riso">RISO</label>
							<input type="checkbox" id="riso"
							name="riso">
						</li>
						<li>
							<label for="ileak">ILEAK</label>
							<input type="checkbox" id="ileak"
							name="ileak">
						</li>
						<li>
							<label for="genfreq">GENFREQ</label>
							<input type="checkbox" id="genfreq"
							name="genfreq">
						</li>
					</ul>
					<ul>
						<li>
							<label for="temp">Temperature</label>
							<input type="checkbox" id="temp"
							name="temp">
						</li>
						<li>
							<label for="relative-humidity">Relative Humidity</label>
							<input type="checkbox" id="relative-humidity"
							name="relative-humidity">
						</li>
						<li>
							<label for="dewpoint">Dewpoint</label>
							<input type="checkbox" id="dewpoint"
							name="dewpoint">
						</li>
						<li>
							<label for="wind-heading">Wind Heading</label>
							<input type="checkbox" id="wind-heading"
							name="wind-heading">
						</li>
						<li>
							<label for="wind-speed">Wind Speed</label>
							<input type="checkbox" id="wind-speed"
							name="wind-speed">
						</li>
						<li>
							<label for="pressure">Pressure</label>
							<input type="checkbox" id="pressure"
							name="pressure">
						</li>
					
					</ul>
				</fieldset>
			</section>
			<br>
			<input type="submit" name="submit" value="Submit">
		</form>


	

		
	</body>
	
	
</html>