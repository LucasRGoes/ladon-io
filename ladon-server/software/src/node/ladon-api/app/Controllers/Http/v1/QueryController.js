'use strict'

const Package = use('App/Models/Package')
const Logger = use('Logger')

class QueryController {

	async range({ request, params }) {

		// Stores range parameters
		Logger.info("Range requested")
		const to = request.input('to', Math.floor(Date.now() / 1000))
		const from = request.input('from', to - 86400)

		return await Package.find({ id: params.id, description: params.description, sentOn: { '$gte': from, '$lt': to } })
							.sort({ sentOn: -1 })

	}

	async last({ request, params }) {

		Logger.info("Last requested")
		return await Package.find({ id: params.id, description: params.description })
							.sort({ sentOn: -1 })
							.limit(1)

	}

	async list({ request }) {

		Logger.info("List requested")
		return await Package.aggregate([
			{ 
				'$group': {
					_id: { id: '$id' },
					descriptions: { '$addToSet': '$description' }
				} 
			}
		])

	}

}

module.exports = QueryController
