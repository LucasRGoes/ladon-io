'use strict'

const Package            = use('App/Models/PackageV2')
const Drive  			 = use('Drive')
const Helpers 			 = use('Helpers')
const Logger             = use('Logger')
const RipeningClassifier = use('RipeningClassifier')
const DataExtractor      = use('DataExtractor')

class QueryController {

	async range({ request, params }) {

		// Stores range parameters
		const to = request.input('to', Math.floor(Date.now()))
		const from = request.input('from', to - 86400000)
		Logger.info(`Range requested for ${params.device} at feature ${params.feature} from ${from} to ${to}`)

		return await Package.find({ device: params.device, feature: params.feature, sentOn: { '$gte': from, '$lt': to } })
							.sort({ sentOn: -1 })

	}

	async last({ request, params }) {

		Logger.info(`Last requested for ${params.device} at feature ${params.feature}`)
		return await Package.find({ device: params.device, feature: params.feature })
							.sort({ sentOn: -1 })
							.limit(1)

	}

	async list({ request }) {

		Logger.info("List requested")
		return await Package.aggregate([
			{ 
				'$group': {
					_id: { id: '$device' },
					features: { '$addToSet': '$feature' }
				} 
			}
		])

	}

	async process({ request }) {

		// Stores classify parameters
		const image = request.input('image')
		Logger.info("Process requested")

		await Drive.put( Helpers.tmpPath('uploads/toProcess.png'), Buffer.from(image, 'base64') )

		const filePath = Helpers.tmpPath('uploads/toProcess.png')
		const processedImage =  await DataExtractor.extract(filePath)
		await Drive.delete(filePath)

		return processedImage

	}

	async classify({ request }) {

		// Stores classify parameters
		const bMax = request.input('b_max')
		const aMax = request.input('a_max')
		const aMin = request.input('a_min')
		const lMedian = request.input('L_median')
		Logger.info("Classify requested")

		return await RipeningClassifier.classify(bMax, aMax, aMin, lMedian)

	}

}

module.exports = QueryController
