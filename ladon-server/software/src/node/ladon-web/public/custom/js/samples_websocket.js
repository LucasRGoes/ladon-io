/* Websocket */
let ws = null

let lastExtractedData = {
	receivedResponse: 0,
	extractedData: {
		'b_max': 	null,
		'a_max': 	null,
		'a_min': 	null,
		'L_median': null
	}
}

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
						case 'photo':
							dashboardValue.setAttribute( 'src', `${ data.value.replace('/var/log/ladon/', '') }` )
							break
						case 'b_max':
						case 'a_max':
						case 'a_min':
						case 'L_median':
							lastExtractedData.receivedResponse++
							lastExtractedData.extractedData[feature] = parseFloat(data.value)
							break
					}
					dashboardTimestamp.innerHTML = moment(data.sentOn).fromNow()

				}
				break
			case 'classify':
				if(message.status) {

					// Getting data
					const data = message.data[0]
					
					// Storing HTML element
					const dashboardValue = document.getElementById('maturity')

					// Setting value
					dashboardValue.innerHTML = `${ data.maturity }`

				}
				break

		}

	})

	// Starts by requesting the first batch of last data
	requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 3) // Photo
	requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 4) // b* Max
	requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 5) // a* Max
	requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 6) // a* Min
	requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 7) // L* Median

	// Setting intervals for subsequent requests
	setInterval(() => requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 3), 60 * 60 * 1000) 	// 1 hour
	setInterval(() => {
		requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 4) // b* Max
		requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 5) // a* Max
		requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 6) // a* Min
		requestData(ws, 'ladon', 'last', 'nZyLYVd9bBcfeuAm', 7) // L* Median
	}, 60 * 60 * 1000) 	// 1 hour
	setInterval(() => {

		if(lastExtractedData.receivedResponse >= 4) {
			requestData(ws, 'ladon', 'classify', null, lastExtractedData.extractedData) // Classification
			lastExtractedData.receivedResponse = 0
		}

	}, 3 * 1000) // 3 seconds

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
