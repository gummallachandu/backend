
p=function (arr) {
  console.log(arr);
}
  
d=function (arr) {
  console.log(arr);
  process.exit();
}
  
sendMail = function(to,mailSubject, mailBody, callback) {
  const nodemailer = require('nodemailer');
  
  var smtpTransport = nodemailer.createTransport({
        host: 'mail.textmercato.com',
        port: 587,
        auth: {
            user: 'ramesh.textmercato',
            pass: 'ramesh123'
        },
        tls: {rejectUnauthorized: false} 
    });
    
  var mailOptions = {
    to: to,
    from: 'admin@textmercato.com',
    subject: mailSubject,
    html: mailBody
  };
  smtpTransport.sendMail(mailOptions, function (err) {
    if (!err) {
      callback(null,'success');
    } else {
      callback(err,'fail');
    }
  });
}

