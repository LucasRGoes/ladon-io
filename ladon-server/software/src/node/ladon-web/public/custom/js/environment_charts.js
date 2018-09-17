/* Graphs */
const temperatureCtx = document.getElementById('temperature_graph').getContext('2d')
const humidityCtx 	 = document.getElementById('humidity_graph').getContext('2d')

const temperatureChart = new Chart(temperatureCtx, {
	type: 'line',
	data: {
		labels: [],
		datasets: [{
            label: 'Temperature(°C)',
            borderColor: 'rgb(220, 20, 60)',
            data: [],
        }]
	},
	options: {},
	responsive: true
})

const humidityChart = new Chart(humidityCtx, {
	type: 'line',
	data: {
		labels: [],
		datasets: [{
            label: 'Humidity(%)',
            borderColor: 'rgb(30, 144, 255)',
            data: [],
        }]
	},
	options: {},
	responsive: true
})

const updateChart = (chart, labels, data) => {
	chart.data.labels = labels
	chart.data.datasets[0].data = data
	chart.update()
}
