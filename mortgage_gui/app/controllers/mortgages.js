var mongoose = require('mongoose'),
    Mortgage = mongoose.model('Mortgage');

exports.index = function(req, res){
  Mortgage.find(function(err, mortgages){
    if(err) throw new Error(err);
    res.render('mortgages/index', {
      title: 'Mortgage Calculator',
      mortgages: mortgages
    });
  });
};

exports.show = function(req, res) {
  Mortgage.findById(req.params.id, function(err, mortgage) {
    if (err)
      throw err;
    res.render('mortgages/show', {
      mortgage: mortgage,
      title: mortgage.name
    }); 
  });
};

exports.new = function(req, res) {
  res.render('mortgages/new');
};

exports.create = function(req, res) {
  new Mortgage({
    // name: req.body.name,
    // email: req.body.email,
    // telephone: req.body.telephone,
  }).save(function(err, mortgage){
    if (err)
      throw err;
    res.redirect('/mortgages');
  });
};

exports.destroy = function(req, res) {
  Mortgage.findById(req.params.id, function(err, mortgage){
    customer.remove(function(err, mortgage){
      if (err)
        throw err;
      res.redirect('mortgages/index');
    });
  });
};