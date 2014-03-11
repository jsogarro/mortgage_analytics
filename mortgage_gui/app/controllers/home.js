var mongoose = require('mongoose'),
  Mortgage = mongoose.model('Mortgage');

exports.index = function(req, res) {
  res.render('home/index');
}