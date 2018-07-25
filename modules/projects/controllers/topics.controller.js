'use strict';

/**
 * Module dependencies
 */
var path = require('path'),
  mongoose = require('mongoose'),
  Topic = mongoose.model('Topic'),
  errorHandler = require(path.resolve('./modules/core/controllers/errors.controller'));

//require(path.resolve('./modules/common'));
/**
 * Show the current user
 */
exports.read = function (req, res) {
  res.json({"status":"success","data":req.model});
};

exports.create = function (req, res) {
  var topic = new Topic(req.body);
  topic.status = 1;
  
  topic.save(function (err) {
    if (err) {
      return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
    }
    res.json({"status":"success"});
  });
};

/**
 * Update a Topic
 */
exports.update = function (req, res) {
  var topic = req.model;
  topic.topic = req.body.topic;
  if(req.body.status) topic.status = req.body.status;
  
  topic.save(function (err) {
    if (err) {
      return res.status(422).send({
        message: errorHandler.getErrorMessage(err)
      });
    } else {
      res.json({"status":"success"});
    }
  });
};

/**
 * Delete a Topic
 */
exports.delete = function (req, res) {
  var topic = req.model;

  topic.remove(function (err) {
    if (err) {
      return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
    }

    res.json({"status":"success"});
  });
};

/**
 * List of Topics
 */
exports.list = function (req, res) {
  var cond = {"status":1},fields = 'topic';
  
  if (req.user && req.user.roles.indexOf('admin') != -1){
    cond = {};
    fields = '';
  }
  
  Topic.find(cond,fields).exec(function (err,topics) {
    if (err) {
      return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
    }
    res.json({"status":"success","data":topics});
  });
};



/**
 * Topic middleware
 */
exports.topicIdByID = function (req, res, next, id) {
  if (!mongoose.Types.ObjectId.isValid(id)) {
    return res.status(400).send(errorHandler.getJsonError('invalid_project'));
  }

  Topic.findById(id).exec(function (err, topic) {
    if (err) {
      return next(err);
    } else if (!Topic) {
      return next(new Error('Failed to load topic ' + id));
    }

    req.model = topic;
    next();
  });
};
