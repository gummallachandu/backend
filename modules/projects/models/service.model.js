'use strict';

/**
 * Module dependencies
 */
var mongoose = require('mongoose'),
  Schema = mongoose.Schema,
  path = require('path'),
  config = require(path.resolve('./config/config'));

/**
 * Article Schema
 */
var ServiceSchema = new Schema({
  created: {
    type: Date,
    default: Date.now
  },
  title: {
    type: String,
    default: '',
    trim: true,
    required: 'Service Name cannot be blank'
  },
  price_per_word:{
    type: Number,
    default: 0,
    trim: true,
    required: 'Service Price cannot be blank'
  },
  status:{
    type: Number,
    default: 0
  }
});


mongoose.model('Service', ServiceSchema);
