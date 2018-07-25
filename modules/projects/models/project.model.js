'use strict';

/**
 * Module dependencies
 */
var mongoose = require('mongoose'),
  path = require('path'),
  config = require(path.resolve('./config/config')),
  Schema = mongoose.Schema,
  validator = require('validator');

var ProjectSchema = new Schema({
  prj_name: {
    type: String,
    default: '',
    required: 'Please fill project name',
  },
  client: {
    type: Schema.ObjectId,
    ref: 'User'
  },
  divisions:[],
  price_per_word:{
    type: Number,
    default: 0,
    trim: true,
  },
  total_amount:{
    type: Number
  },
  due_date:{
    type: Date
  },
  delivery_date:{
    type: Date
  },
  updated: {
    type: Date
  },
  created: {
    type: Date,
    default: Date.now
  },
  freeze:{
    type: Boolean,
    default: 0
  },
  status:{
    type: Number,
    default: 0
  }
});

mongoose.model('Project', ProjectSchema);
