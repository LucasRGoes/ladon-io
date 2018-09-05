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

		Route.get('id/:id/description/:description', 		'v1/QueryController.range')
		Route.get('id/:id/description/:description/last', 	'v1/QueryController.last')
		Route.get('list', 									'v1/QueryController.list')

	})
	.prefix('api/v1')
	.middleware(['auth'])

Route
	.group(() => {

		Route.get('device/:device/feature/:feature', 		'v2/QueryController.range')
		Route.get('device/:device/feature/:feature/last', 	'v2/QueryController.last')
		Route.get('list', 									'v2/QueryController.list')
		Route.post('classify',								'v2/QueryController.classify')

	})
	.prefix('api/v2')
	.middleware(['auth'])
