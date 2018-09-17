'use strict'

const { ServiceProvider } = require('@adonisjs/fold')

class RipeningClassifierProvider extends ServiceProvider {
  /**
   * Register namespaces to the IoC container
   *
   * @method register
   *
   * @return {void}
   */
  register () {
    this.app.singleton('Ladon/Addons/RipeningClassifier', () => {
      return new (require('.'))()
    })
  }
}

module.exports = RipeningClassifierProvider
