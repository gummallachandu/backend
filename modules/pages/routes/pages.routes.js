'use strict';

var pages = require('../controllers/pages.controller'),
    path = require('path'),
    core = require(path.resolve('./modules/core/controllers/core.controller'));

const validate = require('../validations/pages.validations');

module.exports = function (app) {
    app.route('/contact-us').post(validate.contact_us,pages.contact_us);
}
