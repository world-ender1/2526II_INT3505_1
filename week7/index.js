const config = require('./config');
const logger = require('./logger');
const ExpressServer = require('./expressServer');

const mongoose = require('mongoose');

const launchServer = async () => {
  try {
    await mongoose.connect('mongodb://127.0.0.1:27017/shop');
    logger.info('Connected to MongoDB');

    this.expressServer = new ExpressServer(config.URL_PORT, config.OPENAPI_YAML);
    this.expressServer.launch();
    logger.info('Express server running');
  } catch (error) {
    logger.error('Express Server failure', error.message);
    await this.close();
  }
};

launchServer().catch(e => logger.error(e));
