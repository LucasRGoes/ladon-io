'use strict'

const Drive   = use('Drive')
const Env     = use('Env')
const Logger  = use('Logger')
const Helpers = use('Helpers')
const Batch   = use('App/Models/Batch')
const User    = use('App/Models/User')

const rp = require('request-promise-native')

class UserController {

	async index({ response, view, auth }) {

		try {
			await auth.getUser()
			response.redirect('/environment')
		} catch (error) {
			return view.render('auth.login')
		}

	}

	async environment({ request, view, auth }) {
		request.user = await auth.getUser()
		return view.render('dashboard.environment')
	}

	async samples({ request, view, auth }) {
		request.user = await auth.getUser()
		return view.render('dashboard.samples')
	}

	async batches({ request, view, auth }) {
		request.user = await auth.getUser()
		return view.render('dashboard.batches', { submit: false })
	}

	async addBatch({ request, view, auth }) {
		request.user = await auth.getUser()

		const batchData = request.only(['batch_start', 'batch_end'])

		batchData['batch_start'] = new Date(batchData['batch_start']).getTime()
		batchData['batch_end']   = new Date(batchData['batch_end']).getTime()

		try {
			await Batch.create(batchData)
			Logger.info(`Batch stored`)
			return view.render('dashboard.batches', { submit: true, message: 'Your batch has been succesfully stored!' })
		} catch (error) {
			Logger.error(`Couldn't store batch`, error)
			return view.render('dashboard.batches', { submit: true, message: 'Your batch couldn\'t be stored' })
		}
		
	}

	async example({ request, view, auth }) {
		request.user = await auth.getUser()
		return view.render('dashboard.example')
	}

	async login({ request, response, auth }) {

		const { email, password } = request.only(['email', 'password'])

		try {
			await auth.attempt(email, password)
			Logger.info(`User ${email} logged in`)
		} catch (error) {
			Logger.error(`User ${email} couldn't login`, error)
		} finally {
			response.redirect('/')
		}

	}

	async logout({ response, auth }) {

		try {
			await auth.logout()
			Logger.info(`User logged out`)
		} catch (error) {
			Logger.error(`User couldn't logout`, error)
		} finally {
			response.redirect('/')
		}

	}

	async create({ request, response }) {

		const userData = request.only(['username', 'email', 'password'])

		try {
			await User.create(userData)
			Logger.info(`User ${email} created`)
		} catch (error) {
			Logger.error(`Couldn't create user ${email}`, error)
		} finally {
			response.redirect('/')
		}

	}

	async upload({ request }) {

		const image = request.file('file', {
			types: ['image'],
			size: '5mb'
		})

		const fileName = image['stream']['filename']

		await image.move( Helpers.tmpPath('uploads'), {
			name: fileName
		} )

		if (!image.moved()) {
			return image.error()
		}

		const filePath = Helpers.tmpPath(`uploads/${ fileName }`)

		let encodedFile = await Drive.get(filePath)
		encodedFile = encodedFile.toString('base64')
		await Drive.delete(filePath)

		try {
			const response = await rp({
				url: `${ Env.get('API_URL') }/process`,
				method: 'POST',
				headers: {
					'Authorization': `Bearer ${ Env.get('API_KEY') }`
				},
				json: { image: encodedFile }
			})

			if('draw_image' in response) {
				return response
			} else {
				return 'File too big for processing at our test pipeline!'
			}
		} catch(err) {
			return 'File too big for processing at our test pipeline!'
		}

	}

}

module.exports = UserController
