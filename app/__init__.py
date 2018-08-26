from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

from app import routes, models
