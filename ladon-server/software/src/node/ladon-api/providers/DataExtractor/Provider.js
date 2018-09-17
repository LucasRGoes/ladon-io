'use strict'

const { ServiceProvider } = require('@adonisjs/fold')

class DataExtractorProvider extends ServiceProvider {
  /**
   * Register namespaces to the IoC container
   *
   * @method register
   *
   * @return {void}
   */
  register () {
    this.app.singleton('Ladon/Addons/DataExtractor', () => {
      return new (require('.'))()
    })
  }
}

module.exports = DataExtractorProvider
