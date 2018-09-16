'use strict'

const Schema = use('Schema')

class BatchSchema extends Schema {
  up () {
    this.create('batches', (table) => {
      table.increments()
      table.timestamp('batch_start').defaultTo( this.fn.now() )
      table.timestamp('batch_end').defaultTo( this.fn.now() )
      table.timestamps()
    })
  }

  down () {
    this.drop('batches')
  }
}

module.exports = BatchSchema
