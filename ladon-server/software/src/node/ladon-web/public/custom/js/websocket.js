/* Websocket */
let ws = null
let devices = null

function requestDevices(channel) {
	ws.getSubscription(channel).emit('message', {
		request: 'list'
	})
}

function requestLastData(channel) {
	ws.getSubscription(channel).emit('message', {
		request: 'last'
	})
}

function requestData(channel) {
	ws.getSubscription(channel).emit('message', {
		request: 'time'
	})
}

function subscribeToChannel () {

	const ladon = ws.subscribe('ladon')

	ladon.on('error', () => {
		$('.connection-status').removeClass('connected')
	})

	ladon.on('message', (message) => {

		switch(message.response) {

			case 'list':
				if(message.status) {
					devices = message.data
				} else {
					setTimeout(() => requestDevices('ladon'), 5000)
				}
				break
			case 'last':
				break
			case 'time':
				break

		}
		devices = message
	})

	requestDevices('ladon')
	//setInterval(requestDevices, 10000);

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
