'use strict';

/**
 * Module dependencies
 */
var acl = require('acl'),
  path = require('path'),
  errorHandler = require(path.resolve('./modules/core/controllers/errors.controller'));

//require(path.resolve('./modules/common'));
// Using the memory backend
acl = new acl(new acl.memoryBackend());

/**
 * Invoke Admin Permissions
 */
exports.invokeRolesPolicies = function () {
  acl.allow([{
    roles: ['admin','client'],
    allows: [{
      resources: '/projects',
      permissions: '*'
    }, {
      resources: '/projects/:projectId',
      permissions: '*'
    }]
    },{
    roles: ['writer'],
    allows: [{
      resources: '/projects',
      permissions: ['get']
    }, {
      resources: '/projects/:projectId',
      permissions: ['get']
    }]
  }]);
};

/**
 * Check If Admin Policy Allows
 */
exports.isAllowed = function (req, res, next) {
  var roles = (req.user) ? req.user.roles : ['guest'];

  // Check for user roles
  acl.areAnyRolesAllowed(roles, req.route.path, req.method.toLowerCase(), function (err, isAllowed) {
    if (err) {
      // An authorization error occurred
      return res.status(500).send('Unexpected authorization error');
    } else {
      if (isAllowed) {
        // Access granted! Invoke next middleware
        return next();
      } else {
        return res.status(403).json(errorHandler.getJsonError('not_authorized',err));
      }
    }
  });
};
