'use strict'

const Schema = use('Schema')

class BatchSchema extends Schema {
  up () {
    this.create('batches', (table) => {
      table.increments()
      table.timestamp('batch_start')
      table.timestamp('batch_end')
      table.timestamps()
    })
  }

  down () {
    this.drop('batches')
  }
}

module.exports = BatchSchema
