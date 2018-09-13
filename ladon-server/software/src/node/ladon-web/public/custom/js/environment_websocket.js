/* Websocket */
let ws = null

const subscribeToChannel = () => {

	const ladon = ws.subscribe('ladon')

	/* EVENTS */
	ladon.on('error', () => {
		$('.connection-status').removeClass('connected')
	})

	ladon.on('message', (message) => {

		switch(message.response) {

			case 'last':
				if(message.status) {

					// Getting data and translating feature id to string
					const data    = message.data[0]
					const feature = translateFeature(data.feature)

					// Storing HTML elements
					const dashboardValue     = document.getElementById(feature)
					const dashboardTimestamp = document.getElementById(`${ feature }_timestamp`)

					// Setting value and timestamp
					switch(feature) {
						case 'temperature':
							dashboardValue.innerHTML = `${ parseFloat(data.value).toFixed(2) }°C`
							break
						case 'humidity':
							dashboardValue.innerHTML = `${ parseFloat(data.value).toFixed(2) }%`
							break
					}
					dashboardTimestamp.innerHTML = moment(data.sentOn).fromNow()

				}
				break
			case 'time':
				if(message.status) {

					// Translating sent time and packing data
					let labels = []
					let dataArray = []
					for(let data of message.data) {
						labels.unshift( moment(data.sentOn).format('HH:mm') )
						dataArray.unshift(data.value)
					}
					
					// Filling charts
					const feature = translateFeature(message.data[0].feature)
					switch(feature) {
						case 'temperature':
							updateChart(temperatureChart, labels, dataArray)
							break
						case 'humidity':
							updateChart(humidityChart, labels, dataArray)
							break
					}

				}
				break

		}

	})

	// Starts by requesting the first batch of last data and time data
	requestData(ws, 'ladon', 'last', 'vzyJYkThrw9u9gP5', 1) // Temperature
	requestData(ws, 'ladon', 'time', 'vzyJYkThrw9u9gP5', 1) // Temperature
	requestData(ws, 'ladon', 'last', 'vzyJYkThrw9u9gP5', 2) // Humidity
	requestData(ws, 'ladon', 'time', 'vzyJYkThrw9u9gP5', 2) // Temperature

	// Setting intervals for subsequent requests
	setInterval(() => requestData(ws, 'ladon', 'last', 'vzyJYkThrw9u9gP5', 1), 60 * 1000) 		// 1 minute
	setInterval(() => requestData(ws, 'ladon', 'time', 'vzyJYkThrw9u9gP5', 1), 60 * 60 * 1000) 	// 1 hour
	setInterval(() => requestData(ws, 'ladon', 'last', 'vzyJYkThrw9u9gP5', 2), 60 * 1000) 		// 1 minute
	setInterval(() => requestData(ws, 'ladon', 'time', 'vzyJYkThrw9u9gP5', 2), 60 * 60 * 1000) 	// 1 hour

}

const startChat = () => {

	ws = adonis.Ws().connect()

	ws.on('open', () => {
		$('.connection-status').addClass('connected')
		subscribeToChannel()
	})

	ws.on('error', () => {
		$('.connection-status').removeClass('connected')
	})

}

$(function () {
	startChat()
})
