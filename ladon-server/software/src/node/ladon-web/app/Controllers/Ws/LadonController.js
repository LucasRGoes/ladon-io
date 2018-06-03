'use strict'

const Env = use('Env')
const Logger = use('Logger')

const request = require('request');

class LadonController {

  constructor ({ socket, request }) {

    this.socket = socket
    this.request = request

    this.apiUrl = Env.get('API_URL')
    this.apiHeaders = {
		'Authorization': `Bearer ${ Env.get('API_KEY') }`,
		'Accept': 'application/json'
	}

    Logger.info(`Socket ${ this.socket.id } connected`)

  }
  
  onMessage (message) {

  	Logger.info(`Socket ${ this.socket.id } requested: ${ message.request }`)

  	// Preparing variables to be used
  	const socket = this.socket
  	const requestOptions = {
  		url: this.apiUrl,
  		headers: this.apiHeaders
  	}
  	const answer = {
		response: message.request,
		status: true
	}
  	const requestCallback = (error, response, body) => {
		if (!error && response.statusCode == 200) {
			answer.data = JSON.parse(body)
		} else {
			answer.status = false
		}

		socket.emit('message', answer)
	}

  	// Verifying type of request
  	switch(message.request) {

  		case 'list':
  			requestOptions.url += '/list'
  			request(requestOptions, requestCallback)
  			break
  		case 'last':
  			break
  		case 'time':
  			break

  	}

  }

  onClose () {
    Logger.info(`Socket ${ this.socket.id } closed`)
  }

  onError () {
    Logger.error(`Error at socket ${ this.socket.id }`)
  }

}

module.exports = LadonController
