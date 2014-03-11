var path = require('path'),
    rootPath = path.normalize(__dirname + '/..'),
    env = process.env.NODE_ENV || 'development';

var config = {
  development: {
    root: rootPath,
    app: {
      name: 'mortgage-gui'
    },
    port: 3000,
    db: 'mongodb://localhost/mortgage-gui-development'
  },

  test: {
    root: rootPath,
    app: {
      name: 'mortgage-gui'
    },
    port: 3000,
    db: 'mongodb://localhost/mortgage-gui-test'
  },

  production: {
    root: rootPath,
    app: {
      name: 'mortgage-gui'
    },
    port: 3000,
    db: 'mongodb://localhost/mortgage-gui-production'
  }
};

module.exports = config[env];
