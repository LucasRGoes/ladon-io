/* Websocket */
let ws = null

let classificationResponse = null

const requestClassification = (params) => {

	requestData(ws, 'ladon', 'classify', null, params) // Classification

	return new Promise( (resolve, reject) => {
		const interval = setInterval(() => {

			if(classificationResponse !== null) {
				let response = Object.assign({}, classificationResponse)
				classificationResponse = null

				clearTimeout(interval)
				resolve(response)
			}

		}, 1000) // Each second	
	} )

}

const subscribeToChannel = () => {

	const ladon = ws.subscribe('ladon')

	/* EVENTS */
	ladon.on('error', () => {
		$('.connection-status').removeClass('connected')
	})

	ladon.on('message', (message) => {

		switch(message.response) {

			case 'classify':
				if(message.status) {
					classificationResponse = message.data[0]
				}
				break

		}

	})

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
