'use strict';


var path = require('path'),
  mongoose = require('mongoose'),
  AppController = require(path.resolve('./modules/app_controller'));
  
  
class ServiceController extends AppController{
  constructor(){
    super('service','Service');
    this.init = this.init.bind(this);
    this.plist = this.plist.bind(this);
    this.getPrice = this.getPrice.bind(this);
  }
  
  plist(req, res){
    var cond = {"status":1},fields = 'title';
  
    if (req.user && req.user.roles.indexOf('admin') != -1){
      cond = {};
      fields = '';
    }
    req.db_cond = cond;
    req.db_fields = fields;
    super.list(req,res);
  }
  
  getPrice(req, res, next) {
    var id = req.params.sid;
    var _this = this;
    
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return _this.show_error(res,'invalid_project');
    }
    
    this._model.findById(id,'price_per_word').exec(function (err, service) {
      if (err) {
        return next(err);
      } else if (!service) {
        return _this.show_error(res,'service_not_found');
      }
      res.json({"status":"success","data":service.price_per_word});
    });
  }
}

module.exports = ServiceController;