'use strict'

/*
|--------------------------------------------------------------------------
| Routes
|--------------------------------------------------------------------------
|
| Http routes are entry points to your web application. You can create
| routes for different URL's and bind Controller actions to them.
|
| A complete guide on routing is available here.
| http://adonisjs.com/docs/4.0/routing
|
*/

const Route = use('Route')

//Route.post('/token', 'TokenController.store')

Route
	.group(() => {

		Route.get('id/:id/description/:description', 'QueryController.range')
		Route.get('id/:id/description/:description/last', 'QueryController.last')
		Route.get('list', 'QueryController.list')

	})
	.prefix('api/v1')
	.middleware(['auth'])
