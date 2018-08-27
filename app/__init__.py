from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# create a flask application and assign to app variable
app = Flask(__name__)

# creates app configuration based on our config class
app.config.from_object(Config)

# set static assets folder
app.static_folder = 'static'

# set the db
db = SQLAlchemy(app)

# set the migration engine
migrate = Migrate(app, db)

# handle login and remember me with login manager
login = LoginManager(app)

# access control redirect endpoint
login.login_view = 'login'

# use moment.js for time and date parsing
moment = Moment(app)

# if the application is not in debugging mode
if not app.debug:

  # Email Errors
  # if MAIL_SERVER exists within /config.py
  if app.config['MAIL_SERVER']:
    # set auth to None by default
    auth = None
    # if MAIL_USERNAME or MAIL_PASSWORD exists within /config.py
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
      # set auth to MAIL_USERNAME and MAIL_PASSWORD
      auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    # set secure to None by default
    secure = None
    # if MAIL_USE_TLS exists within /config.py
    if app.config['MAIL_USE_TLS']:
      # set secure
      secure = ()
    # instantiate SMTPHandler to mail_handler
    mail_handler = SMTPHandler(
      mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
      fromaddr='no-reply@' + app.config['MAIL_SERVER'],
      toaddrs=app.config['ADMINS'],
      subject='OpenFoundry API Failure',
      credentials=auth,
      secure=secure) 
    # log importance level
    # https://docs.python.org/3.1/library/logging.html
    mail_handler.setLevel(logging.ERROR)
    # add mail_handler to app logging
    app.logger.addHandler(mail_handler)
    # log errors to file
    # if /logs directory does not exist
    if not os.path.exists('logs'):
      # create /logs directory
      os.mkdir('logs')
    # instantiate RotatingFileHandler to file_handler
    # max size 10k
    # last 10 errors kept  
    file_handler = RotatingFileHandler('logs/openfoundry.log', maxBytes=10240, backupCount=10)
    # format how the error logs are written
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # log importance level
    file_handler.setLevel(logging.INFO)
    # add file_handler to app logging
    app.logger.addHandler(file_handler)
    # app level log importance level
    app.logger.setLevel(logging.INFO)
    # log when app starts
    app.logger.info('OpenFoundry Started')    
# instantiate routes, models, errors
from app import routes, models, errors