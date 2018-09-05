/* Websocket */
let ws = null

function requestData(channel, request, device = null, feature = null) {
	ws.getSubscription(channel).emit('message', {
		request: request,
		device: device,
		feature: feature
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
						const deviceId = device._id.id
						for(let feature of device.features) {
							requestData('ladon', 'last', deviceId, feature)
							setInterval(() => requestData('ladon', 'last', deviceId, feature), 60 * 1000) 	 // 60 seconds
							requestData('ladon', 'time', deviceId, feature)
							setInterval(() => requestData('ladon', 'time', deviceId, feature), 30 * 60 * 1000) // 30 minutes
						}
					}
				} else {
					setTimeout(() => requestData('ladon', 'list'), 10 * 1000) // 10 seconds
				}
				break
			case 'last':
				if(message.status) {
					const data = message.data[0]
					const feature = translateFeature(data.feature)

					const dashboardValue = document.getElementById(feature)
					const dashboardTimestamp = document.getElementById(`${ feature }_timestamp`)

					if(dashboardValue && dashboardTimestamp) {

						switch(feature) {
							case 'photo':
								dashboardValue.setAttribute( 'src', `${ data.value.replace('/var/log/ladon/', '') }` )
								break
							case 'temperature':
								dashboardValue.innerHTML = `${ parseFloat(data.value).toFixed(2) }°C`
								break
							case 'humidity':
								dashboardValue.innerHTML = `${ parseFloat(data.value).toFixed(2) }%`
								break
						}

						dashboardTimestamp.innerHTML = moment(data.sentOn).fromNow()
					}
				}
				break
			case 'time':
				if(message.status) {

					let labels = []
					let dataArray = []
					for(let data of message.data) {
						labels.unshift( moment(data.sentOn).format('HH:mm') )
						dataArray.unshift(data.value)
					}
					
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
