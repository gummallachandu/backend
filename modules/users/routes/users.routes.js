'use strict';

module.exports = function (app) {
  // User Routes
  var users = require('../controllers/users.controller'),
    path = require('path'),
    core = require(path.resolve('./modules/core/controllers/core.controller'));

  // Setting up the users profile api
  app.route('/users/me').get(users.me);
  app.route('/users').put(users.update);
  app.route('/users/accounts').delete(users.removeOAuthProvider);
  app.route('/users/password').post(users.changePassword);
  app.route('/users/picture').post(users.changeProfilePicture);

  // Finish by binding the user middleware
  app.param('userId', users.userByID);
  
  app.route('/users/*').post(core.renderIndex);
};
