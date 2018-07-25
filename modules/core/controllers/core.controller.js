'use strict';

var validator = require('validator'),
  path = require('path'),
  errorHandler = require(path.resolve('./modules/core/controllers/errors.controller')),
  config = require(path.resolve('./config/config'));

/**
 * Render the main application page
 */
exports.renderIndex = function (req, res) {
  var safeUserObject = null;
  if (req.user) {
    safeUserObject = {
      displayName: validator.escape(req.user.displayName),
      provider: validator.escape(req.user.provider),
      username: validator.escape(req.user.username),
      created: req.user.created.toString(),
      roles: req.user.roles,
      profileImageURL: req.user.profileImageURL,
      email: validator.escape(req.user.email),
      lastName: validator.escape(req.user.lastName),
      firstName: validator.escape(req.user.firstName),
      additionalProvidersData: req.user.additionalProvidersData
    };
  }
  res.json(errorHandler.getJsonError('bad_request'));
  /*res.render('modules/core/views/index', {
    user: JSON.stringify(safeUserObject),
    sharedConfig: JSON.stringify(config.shared)
  });*/
};

/**
 * Render the server error page
 */
exports.renderServerError = function (req, res) {
  res.status(500).json(errorHandler.getJsonError('500_error'));
  /*res.status(500).render('modules/core/views/500', {
    error: 'Oops! Something went wrong...'
  });*/
};

/**
 * Render the server not found responses
 * Performs content-negotiation on the Accept HTTP header
 */
exports.renderNotFound = function (req, res) {
  res.status(404).json(errorHandler.getJsonError('404_error'));
  /*res.status(404).format({
    'text/html': function () {
      res.render('modules/core/views/404', {
        url: req.originalUrl
      });
    },
    'application/json': function () {
      res.json({
        error: 'Path not found'
      });
    },
    'default': function () {
      res.send('Path not found');
    }
  });*/
};
