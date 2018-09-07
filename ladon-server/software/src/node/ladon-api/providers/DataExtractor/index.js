'use strict'

const spawn = require('await-spawn')

class DataExtractorService {

  constructor () {}

  async extract(encodedImage) {

  	try {
	  	let response = await spawn('python3', ['/usr/share/ladon/data-extractor/DataExtractor.py', encodedImage])
	    
	    // Cleaning procedures
	    response = response.toString('utf8')
	    response = JSON.parse(response)

	    return response
	} catch(err) {
		return err.stderr.toString('utf8')
	}

  }

}

module.exports = DataExtractorService
