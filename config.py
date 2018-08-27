import os

# get absolute path of current directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  
  # set debugging to True to show errors on the screen, rather than Bad Gateway message
  DEBUG = False

  # set secret key
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-string-here'
  
  # path to db
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  
  # app does not need to be notified on every database update
  SQLALCHEMY_TRACK_MODIFICATIONS = False  

  # Email Server 
  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  ADMINS = ['adminemail@example.com']  

