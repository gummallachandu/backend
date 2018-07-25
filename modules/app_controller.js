'use strict';

var path = require('path'),
  mongoose = require('mongoose'),
  errorHandler = require(path.resolve('./modules/core/controllers/errors.controller'));

require(path.resolve('./modules/common'));

class AppController {
  
  constructor(controller_name,model_name) {
      //this.create = this.create.bind(this);
      //this.list = this.list.bind(this);
      
      this._model = mongoose.model(model_name);
      this._cname = controller_name;
      this.errors = {}
   }
   
   init(){
      this.create = this.create.bind(this);
      this.update = this.update.bind(this);
      this.list = this.list.bind(this);
      this.getByID = this.getByID.bind(this);
      this.show_error = this.show_error.bind(this);
   }
   
  read(req, res, id) {
    res.json({"status":"success","data":req.model});
  }
   
  create(req, res, next) {
    var smodel = new this._model(req.body);
    
    smodel.save(function (err) {
      if (err) {
        return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
      }
      res.json({"status":"success"});
    });
  }
  
  update(req, res, data) {
    var umodel = req.model;
    
    umodel.save(function (err) {
      if (err) {
        return res.status(422).send({
          message: errorHandler.getErrorMessage(err)
        });
      } else {
        res.json({"status":"success"});
      }
    });
  }
  
  list(req, res) {
    //console.log(this._cname);
    var cond = req.db_cond;
    var fields = req.db_fields;
    
    this._model.find(cond, fields).exec(function (err, data_rows) {
      if (err) {
        return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
      }
      res.json({"status":"success","data":data_rows});
    });
  }
  
  delete(req, res) {
    var dmodel = req.model;
  
    dmodel.remove(function (err) {
      if (err) {
        return res.status(422).send(errorHandler.getJsonError(errorHandler.getErrorMessage(err),err));
      }
  
      res.json({"status":"success"});
    });
  }
  
  getByID(req, res, next, id) {
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).send(errorHandler.getJsonError('invalid ' + _name));
    }
  
    this._model.findById(id).exec(function (err, model_data) {
      if (err) {
        return next(err);
      } else if (!model_data) {
        return next(new Error('Failed to load ' + id));
      }
  
      req.model = model_data;
      next();
    });
  }
  
  show_error(res,err_msg){
    return res.status(422).send(errorHandler.getJsonError(err_msg));
  }

}

module.exports = AppController;