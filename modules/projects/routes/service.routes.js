'use strict';

var ServiceController = require('../controllers/services.controller'),
    servicesPolicy = require('../policies/services.policy'),
    path = require('path'),
    core = require(path.resolve('./modules/core/controllers/core.controller'));

module.exports = function (app) {
  
  const services = new ServiceController();
  services.init();
  
  app.route('/services').all(servicesPolicy.isAllowed)
    .get(services.plist)
    .post(services.create);

  // Single service routes
  app.route('/services/:serviceId').all(servicesPolicy.isAllowed)
    .get(services.read)
    .put(services.update)
    .delete(services.delete);
    
  app.route('/services/price/:sid').get(servicesPolicy.isAllowed,services.getPrice);

  // Finish by binding the service middleware
  app.param('serviceId', services.getByID);
  
  app.route('/services/*').post(core.renderIndex);
};
