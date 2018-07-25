'use strict';

var topics = require('../controllers/topics.controller'),
    topicsPolicy = require('../policies/topics.policy'),
    path = require('path'),
    core = require(path.resolve('./modules/core/controllers/core.controller'));

module.exports = function (app) {

  app.route('/topics').all(topicsPolicy.isAllowed)
    .get(topics.list)
    .post(topics.create);

  // Single article routes
  app.route('/topics/:topicId').all(topicsPolicy.isAllowed)
    .get(topics.read)
    .put(topics.update)
    .delete(topics.delete);

  // Finish by binding the service middleware
  app.param('topicId', topics.topicIdByID);
  
  app.route('/topics/*').post(core.renderIndex);
};
