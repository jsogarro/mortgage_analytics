// Example model

var mongoose = require('mongoose'),
  Schema = mongoose.Schema;

var MortgageSchema = new Schema({
  periods: Number, 
  cusip: String,
  pool_num: String,
  maturity: Date,
  wac: Number,
  wa_credit_score: Number,
  prepmt_penalty: Boolean,
  wa_loan_size: Number,
  ltv: Number,
  name: String,
  rate: Number, 
  pv: Number, 
  pmt: Number,
  fv: Number, 
  mode: String
});

MortgageSchema.virtual('date')
  .get(function(){
    return this._id.getTimestamp();
  });

mongoose.model('Mortgage', MortgageSchema);
