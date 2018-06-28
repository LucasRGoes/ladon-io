'use strict'

const mongoose = use('Mongoose')
const ObjectId = mongoose.Schema.Types.ObjectId
const Mixed = mongoose.Schema.Types.Mixed

let packageSchema = mongoose.Schema({

	path: String,
	id: String,
	type: String,
	description: String,
	value: String,
	timestamp: Number,
	arrival: Number

})
 
module.exports = mongoose.model('Package', packageSchema)