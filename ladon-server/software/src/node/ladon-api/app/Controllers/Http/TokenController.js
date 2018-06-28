'use strict'

const User = use('App/Models/User')

class TokenController {

	async store({ request, auth }) {

		// Stores variables and validates them
		const { username } = request.only(['username'])
		if(!username) {
			return { status: 400, message: 'username missing' }
		}

		// Finds user
		let user
		try {
			user = await User.findByOrFail('username', username)
		} catch(error) {
			return { status: 400, message: 'username invalid' }
		}

		// Generates a token for the user
		return await auth.generate(user)

	}

}

module.exports = TokenController
