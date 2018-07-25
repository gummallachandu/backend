'use strict';

/**
 * Module dependencies
 */
var mongoose = require('mongoose'),
  Schema = mongoose.Schema,
  path = require('path'),
  config = require(path.resolve('./config/config'));

/**
 * Config Schema
 */
var ConfigSchema = new Schema({
  display_text: {
    type: String,
    default: '',
    trim: true,
    required: 'Title cannot be blank'
  },
  desc: {
    type: String,
    default: '',
    trim: true,
    required: 'Description cannot be blank'
  },
  key: {
    type: String,
    unique: 'key already exists',
    trim: true,
    required: 'Key cannot be blank'
  },
  value: {
    type: String,
    default: '',
    trim: true
  },
  default_value: {
    type: String,
    default: '',
    trim: true,
    required: 'Default value cannot be blank'
  },
  field_type: {
    type: String,
    enum:['text','textarea'],
    default: 'text',
  },
  display: {
    type: Boolean,
    default:1
  }
});

mongoose.model('Config', ConfigSchema);
