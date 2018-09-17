'use strict'

const spawn = require('await-spawn')

class DataExtractorService {

  constructor () {}

  async extract(imageUrl) {

  	try {
	  	let response = await spawn('python3', ['/usr/share/ladon/data-extractor/DataExtractor.py', imageUrl])
	  	
	    // Cleaning procedures
	    response = response.toString('utf8')
	    response = JSON.parse(response)

	    return response
	} catch(err) {
		if('stderr' in err) {
			return err.stderr.toString('utf8')
		} else {
			return err
		}
	}

  }

}

module.exports = DataExtractorService
