'use strict'

const spawn = require('await-spawn')

class RipeningClassifierService {

  constructor () {}

  async classify(bMax, aMax, aMin, lMedian) {

  	try {
	  	let response = await spawn('python3', ['/usr/share/ladon/ripening-classifier/RipeningClassifier.py', bMax, aMax, aMin, lMedian])
	    
	    // Cleaning procedures
	    response = response.toString('utf8')
	    response = JSON.parse(response)[0]

	    return [{ maturity: response }]
	} catch(err) {
		return err.stderr.toString('utf8')
	}

  }

}

module.exports = RipeningClassifierService
