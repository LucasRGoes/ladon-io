'use strict'

const Env = use('Env')

module.exports = {
	url: Env.get('MONGO_URL', ''),
	host: Env.get('MONGO_HOST', 'localhost'),
	port: Env.get('MONGO_PORT', '27017'),
	user: Env.get('MONGO_USER', 'root'),
	pass: Env.get('MONGO_PASS', ''),
	db: Env.get('MONGO_DATABASE', 'adonis')
}