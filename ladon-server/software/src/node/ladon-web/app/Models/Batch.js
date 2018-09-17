'use strict'

const Model = use('Model')

class Batch extends Model {
	static get visible () {
		return ['batch_start', 'batch_end']
	}
}

module.exports = Batch
