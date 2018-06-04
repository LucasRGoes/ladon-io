/* Websocket */
let ws = null

function requestData(channel, request, id = null, description = null) {
	ws.getSubscription(channel).emit('message', {
		request: request,
		id: id,
		description: description
	})
}

function subscribeToChannel () {

	const ladon = ws.subscribe('ladon')

	/* EVENTS */
	ladon.on('error', () => {
		$('.connection-status').removeClass('connected')
	})

	ladon.on('message', (message) => {

		switch(message.response) {

			case 'list':
				if(message.status) {
					// For each device found, set an interval for last data pooling
					for(let device of message.data) {
						const id = device._id.id
						for(let description of device.descriptions) {
							requestData('ladon', 'last', id, description)
							setInterval(() => requestData('ladon', 'last', id, description), 60 * 1000)
							requestData('ladon', 'time', id, description)
							setInterval(() => requestData('ladon', 'time', id, description), 30 * 60 * 1000)
						}
					}
				} else {
					setTimeout(() => requestData('ladon', 'list'), 10 * 1000)
				}
				break
			case 'last':
				if(message.status) {
					const data = message.data[0]

					const dashboardValue = document.getElementById(data.description)
					const dashboardTimestamp = document.getElementById(`${ data.description }_timestamp`)

					if(dashboardValue && dashboardTimestamp) {
						dashboardValue.innerHTML = data.value
						dashboardTimestamp.innerHTML = moment(data.timestamp * 1000).fromNow()
					}
				}
				break
			case 'time':
				if(message.status) {

					let labels = []
					let dataArray = []
					for(let data of message.data) {
						labels.unshift(data.timestamp)
						dataArray.unshift(data.value)
					}

					if(message.data[0].description === 'temperature') {
						updateChart(temperatureChart, labels, dataArray)
					} else if(message.data[0].description === 'humidity') {
						updateChart(humidityChart, labels, dataArray)
					}
				}
				break

		}

	})

	// Starts by requesting the list of devices
	requestData('ladon', 'list')

}

function startChat () {

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
