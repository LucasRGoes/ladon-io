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

/* PAGES */
Route.get('/', 'UserController.index')
Route.get('/environment', 'UserController.environment').middleware('auth')
Route.get('/samples', 'UserController.samples').middleware('auth')

/* OTHER ROUTES */
Route.post('/login', 'UserController.login')
Route.get('/logout', 'UserController.logout')
//Route.post('/user', 'UserController.create')
