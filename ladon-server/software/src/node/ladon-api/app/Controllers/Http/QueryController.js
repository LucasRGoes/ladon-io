'use strict'

const Package = use('App/Models/Package')

class QueryController {

	async range({ request, params }) {

		// Stores range parameters
		const to = request.input('to', Math.floor(Date.now() / 1000))
		const from = request.input('from', to - 86400)

		return await Package.find({ id: params.id, description: params.description, timestamp: { '$gte': from, '$lt': to } })
							.sort({ timestamp: -1 })

	}

	async last({ request, params }) {

		return await Package.find({ id: params.id, description: params.description })
							.sort({ timestamp: -1 })
							.limit(1)

	}

	async list({ request }) {

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
