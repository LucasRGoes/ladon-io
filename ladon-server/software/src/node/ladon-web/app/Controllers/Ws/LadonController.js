'use strict'

const Env = use('Env')
const Logger = use('Logger')

const request = require('request')

class LadonController {

  constructor ({ socket, request }) {

    this.socket = socket
    this.request = request

    this.apiUrl = Env.get('API_URL')
    this.apiHeaders = {
      'Authorization': `Bearer ${ Env.get('API_KEY') }`,
      'Accept': 'application/json',
    }

    Logger.info(`Socket ${ this.socket.id } connected`)

  }
  
  onMessage (message) {

  	Logger.info(`Socket ${ this.socket.id } requested: ${ JSON.stringify(message) }`)

  	// Preparing variables to be used
  	const socket = this.socket
  	const requestOptions = {
  		url: this.apiUrl,
  		headers: this.apiHeaders
  	}
  	
  	// Verifying type of request for path completion
  	switch(message.request) {

  		case 'list':
  			requestOptions.url += '/list'
  			break
  		case 'last':
        requestOptions.url += `/device/${ message.device }/feature/${ message.feature }/last`
  			break
  		case 'time':
        const toT = Math.floor(Date.now())
        const fromT = toT - 3600000
        requestOptions.url += `/device/${ message.device }/feature/${ message.feature }?from=${ fromT }&to=${ toT }`
  			break
      case 'classify':
        requestOptions.url += '/classify'
        requestOptions.method = 'POST'
        requestOptions.json = message.feature
        break

  	}

    // Making the request
    request(requestOptions, (error, response, body) => {

      const answer = {
        response: message.request,
        status: true
      }

      if (!error && response.statusCode == 200) {

        try {
          answer.data = JSON.parse(body)
        } catch(err) {
          answer.data = body
        }

      } else {
        answer.status = false
      }

      socket.emit('message', answer)

    })

  }

  onClose () {
    Logger.info(`Socket ${ this.socket.id } closed`)
  }

  onError () {
    Logger.error(`Error at socket ${ this.socket.id }`)
  }

}

module.exports = LadonController
