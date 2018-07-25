'use strict';

/**
 * Module dependencies
 */
var passport = require('passport');

module.exports = function (app) {
  // User Routes
  var users = require('../controllers/users.controller');

  // Setting up the users password api
  app.route('/auth/forgot').post(users.forgot);
  app.route('/auth/reset/:resettoken').get(users.validateResetToken);
  app.route('/auth/reset/:resettoken').post(users.reset);

  // Setting up the users authentication api
  app.route('/signup').post(users.signup);
  app.route('/signin').post(users.signin);
  app.route('/auth/signin').post(users.tokenSignin);
  
  app.route('/signout').get(users.signout);

  // Setting the oauth routes
  app.route('/auth/:strategy').get(users.oauthCall);
  app.route('/auth/:strategy/callback').get(users.oauthCallback);

};
