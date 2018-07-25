'use strict';

var path = require('path'),
  AppController = require(path.resolve('./modules/app_controller'));

class ConfigController extends AppController{
  constructor(){
    super('config','Config');
    this.init = this.init.bind(this);
    this.getKeyVal = this.getKeyVal.bind(this);
    this.getByKey = this.getByKey.bind(this);
  }
  
  getKeyVal(key,callback) {
    this._model.findOne({"key":key},'value').exec(function (err, config) {
      if (err) {
        callback(err,null);
      }else if (config) {
        callback(null,config.value);
      }else {
        callback('config_not_found',null);
      }
    });
  }
  
  getByKey(req, res, next) {
    var key = req.params.key;
    var config_value = '';
    var _this = this;
    if (key == undefined || key == '') {
      res.json({"status":"error","message":"Sorry! Key is required."});
    }else {
      this.getKeyVal(key,function (err,config_value) {
        if (err) {
          _this.show_error(res,err);
        }else{
          res.json({"status":"success","data":config_value});
        }
      });
    }
  }
} 
    
    
module.exports = ConfigController;
