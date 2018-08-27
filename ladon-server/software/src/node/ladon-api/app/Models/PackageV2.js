'use strict'

const mongoose = use('Mongoose')
const ObjectId = mongoose.Schema.Types.ObjectId
const Mixed = mongoose.Schema.Types.Mixed

let packageSchema = mongoose.Schema({

	arrivedOn: Number,
	value: String,
	content: Number,
	feature: Number,
	device: String,
	sentOn: Number

})
 
module.exports = mongoose.model('PackageV2', packageSchema)