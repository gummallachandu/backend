'use strict';

exports.contact_us = function (req,res,next) {
  
  req.checkBody('email', 'Email is required.').notEmpty();
  req.checkBody('email', 'Please enter valid email.').isEmail();
  req.checkBody('fullname', 'Name is required.').notEmpty();
  req.checkBody('mobile', 'Contact Number is required.').notEmpty();
  req.checkBody('mobile', 'Enter valid contact Number.').isMobilePhone("en-IN");
  req.checkBody('comments', 'Your comment is required.').notEmpty();
  
  //req.sanitize('message'); //.xss(); sanitizeBody
  
  const errors = req.validationErrors();
  
  if (errors.length > 0) {
    var msgs = [];
    errors.forEach(function(err){
        msgs.push(err.msg);
    });
    return res.status(422).json({"status":"error", "message": msgs });
  }
  return next();
} 


