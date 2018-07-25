'use strict';

/**
 * Module dependencies
 */
var projectPolicy = require('../policies/projects.policy'),
  project = require('../controllers/projects.controller');

module.exports = function (app) {
  
  // Projects collection routes
  app.route('/projects')
    .post(projectPolicy.isAllowed, project.create)
    .get(projectPolicy.isAllowed, project.list);

  // Single project routes
  app.route('/projects/:projectId')
    .get(projectPolicy.isAllowed, project.read)
    .put(projectPolicy.isAllowed, project.update)
    .delete(projectPolicy.isAllowed, project.delete);

  // Finish by binding the project middleware
  app.param('projectId', project.projectByID);
};
