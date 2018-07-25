'use strict';

var ConfigController = require('../controllers/config.controller'),
    configPolicy = require('../policies/config.policy'),
    path = require('path'),
    core = require(path.resolve('./modules/core/controllers/core.controller'));

module.exports = function (app) {
  
  const config = new ConfigController();
  config.init();
  
  app.route('/config').all(configPolicy.isAllowed)
    .get(config.list)
    .post(config.create);

  // Single service routes
  app.route('/config/:configId').all(configPolicy.isAllowed)
    .get(config.read)
    .put(config.update);
    
  app.route('/config/get/:key').get(configPolicy.isAllowed,config.getByKey);
  
  // Finish by binding the config middleware
  app.param('configId', config.getByID);
  
  app.route('/config/*').post(core.renderIndex);
};
