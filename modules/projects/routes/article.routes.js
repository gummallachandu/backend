'use strict';

/**
 * Module dependencies
 */
var articlesPolicy = require('../policies/articles.policy'),
  articles = require('../controllers/articles.controller');

module.exports = function (app) {
  // Articles collection routes
  app.route('/articles/:projectId').all(articlesPolicy.isAllowed)
    .get(articles.list)
    .post(articles.create);

  // Single article routes
  app.route('/articles/:projectId/:articleId').all(articlesPolicy.isAllowed)
    .get(articles.read)
    .put(articles.update)
    .delete(articles.delete);

  // Finish by binding the article middleware
  app.param('articleId', articles.articleByID);
};
