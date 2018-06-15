'use strict'

const User = use('App/Models/User')
const Logger = use('Logger')

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

}

module.exports = UserController
