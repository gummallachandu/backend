'use strict';

var path = require('path'),
  config = require(path.resolve('./config/config')),
  //cnf = mongoose.model('Config'),
  async = require('async'),
  AppController = require(path.resolve('./modules/app_controller'));
  

exports.contact_us = function (req, res, next) {
    var reply = {"status":"error"};
    async.waterfall([
      function (done) {
          res.render(path.resolve('./modules/pages/templates/contact-us-email'), {
            email: req.body.email,
            name: req.body.fullname,
            mobile: req.body.mobile,
            company: req.body.company,
            comments: req.body.comments
          }, function (err, emailHTML) {
            done(err, emailHTML);
          });
      },
      function (emailHTML, done) {
        sendMail(config.mailer.from,'contact us form submitted',emailHTML,function (err,status) {
            done(err,status);
        });
      }
    ],function (err,status) {
        res.json({"status":status,"message":err});
        next();
    });
    //res.json(reply);
}