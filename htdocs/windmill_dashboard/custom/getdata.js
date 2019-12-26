$(document).ready(function(){
	initGraphs();
	update();
	setInterval(update, 60000);
});

var mainPageLineGraph;
var firstUpdate = 1;

function initGraphs() {
	$.ajax({
		url:"http://localhost/windmill_dashboard/custom/getdata.php",
	type:"GET"})
		.done(function(data){
			var timestamp = [];
			var instantPower = [];
			for(var idx in data) {
				timestamp.push(data[idx].time_stamp.substring(5,16));
				instantPower.push(data[idx].PAC);
			}
			var mainPageChartConfig = {
				type: 'line',
				options: {
					maintainAspectRatio: false,
					responsive: true,
					scales: {
						yAxes: [{
							scaleLabel: {
								display: true,
								labelString: 'Power'
							}
						}],
						xAxes: [{
							scaleLabel: {
								display: true,
								labelString: 'Time'
							}
						}]
					}
				},
				data: {
					labels: timestamp,
					datasets: 
						[{	label:"Instantaneous Power",
							fill:false,
							lineTension:0.1,
							backgroundColor: "rgba(59, 89, 152, 0.75)",
							borderColor: "rgba(59, 89, 152, 1)",
							pointHoverBackgroundColor: "rgba(59, 89, 152, 1)",
							pointHoverBorderColor: "rgba(59, 89, 152, 1)",
							data: instantPower,
						}]
						
				}
			};
			
			var ctx = $("#mainPageLineGraph");
			mainPageLineGraph = new Chart(ctx, mainPageChartConfig);
			mainPageLineGraph.update();
			
		})
		.fail(function(data) { 
			console.log("bad");
			console.log(data);
		})
}



function update() {
	
	$.ajax({
		url:"http://localhost/windmill_dashboard/custom/updateData.php",
	type:"GET"})
		.done(function(data){
			
			console.log("updating");
			
			var dateElement = document.getElementById("date");
			var tempElement = document.getElementById("temp_c");
			var windSpeedElement = document.getElementById("wind_speed");
			var windHeadingElement = document.getElementById("wind_heading");
			var humidityElement = document.getElementById("humidity");
			var dewpointElement = document.getElementById("dewpoint_c");
			var pressureElement = document.getElementById("pressure");
			
			var powerElement = document.getElementById("power");
			var energyElement = document.getElementById("energy_today");
			var percentPowerElement = document.getElementById("percent_power_usage");
			

			if(firstUpdate == 1) {
				firstUpdate = 0;
			} else {
				// update graph
			
				mainPageLineGraph.data.labels.push(data[0].time_stamp.substring(5,16));
				mainPageLineGraph.data.datasets[0].data.push(data[0].PAC);
				mainPageLineGraph.data.labels.shift();
				mainPageLineGraph.data.datasets[0].data.shift();
				mainPageLineGraph.update();
			}
				

				
			/*
			lineChartElement.labels.shift();
			lineChartElement.datasets[0].data.shift();
			chart.update(); */

			newDate = new Date(data[0].time_stamp);
			
			dateElement.innerHTML = newDate.toString().substring(0,21);
			tempElement.innerHTML = data[0].temp_celsius + ' °C';
			windSpeedElement.innerHTML = 'Windspeed: ' + data[0].windspeed_mph + ' mph';
			windHeadingElement.innerHTML = 'Wind Heading: ' + data[0].wind_heading + '°';
			humidityElement.innerHTML = 'Humidity: ' + data[0].relative_humidity + '%';
			dewpointElement.innerHTML = 'Dewpoint: ' + data[0].dewpoint_celsius + ' °C';
			pressureElement.innerHTML = 'Pressure: ' + data[0].pressure_mb + ' mbar';
			powerElement.innerHTML = 'Instantaneous Power: ' + data[0].PAC + ' W';
			energyElement.innerHTML = 'Energy generated today: ' + data[0].ENERGY + ' Wh';
			
			var percentPower = (data[0].ENERGY / 30000 * 100);
            var fixedPercent = percentPower.toFixed(2);
			percentPowerElement.innerHTML = fixedPercent + '%';
			
		})
		.fail(function(data) { 
			console.log("bad");
			console.log(data);
		})
	
	
}