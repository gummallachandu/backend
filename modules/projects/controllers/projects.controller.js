'use strict';

/**
 * Module dependencies
 */
var path = require('path'),
  mongoose = require('mongoose'),
  Project = mongoose.model('Project'),
  errorHandler = require(path.resolve('./modules/core/controllers/errors.controller'));

/**
 * Show the current project
 */
exports.read = function (req, res) {
  res.json({"status":"success","data":req.model});
};

exports.create = function (req, res) {
  var project = new Project(req.body);
  project.client = req.user;
  project.status = 1;
  
  project.save(function (err) {
    if (err) {
      return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
    }
    res.json({"status":"success"});
  });
}

/**
 * Update a project
 */
exports.update = function (req, res) {
  var project = req.model;

  project.save(function (err) {
    if (err) {
      return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
    }
    res.json({"status":"success"});
  });
};

/**
 * Delete a project
 */
exports.delete = function (req, res) {
  var project = req.model;

  project.remove(function (err) {
    if (err) {
      return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
    }

    res.json({"status":"success"});
  });
};

/**
 * List of projects
 */
exports.list = function (req, res) {
  var cond = {},fields='';
  Project.find(cond,fields).sort('-created').exec(function (err, projects) {
    if (err) {
      return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
    }

    res.json({"status":"success","data":projects});
  });
};

/**
 * project middleware
 */
exports.projectByID = function (req, res, next, id) {
  if (!mongoose.Types.ObjectId.isValid(id)) {
    return res.status(400).send(errorHandler.getJsonError('invalid_project'));
  }

  Project.findById(id).exec(function (err, project) {
    if (err) {
      return next(err);
    } else if (!project) {
      return next(new Error('Failed to load project ' + id));
    }

    req.model = project;
    next();
  });
};
