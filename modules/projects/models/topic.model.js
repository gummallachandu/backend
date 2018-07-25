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
var TopicSchema = new Schema({
  created: {
    type: Date,
    default: Date.now
  },
  topic: {
    type: String,
    default: '',
    trim: true,
    required: 'Topic cannot be blank'
  },
  status:{
    type: Number,
    default: 0
  }
});

mongoose.model('Topic', TopicSchema);
