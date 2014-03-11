module.exports = function(app){
	//home route
	var home = require('../app/controllers/home');
	var mortgages = require('../app/controllers/mortgages');

	app.get('/', home.index);
	app.get('/mortgages', mortgages.index);
	app.get('/mortgages/new', mortgages.new);
	app.get('/mortgages/:id', mortgages.show);
	app.get('/mortgagess/delete/:id', mortgages.destroy);
};
