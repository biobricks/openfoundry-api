from flask import Flask
from config import Config
import sqlite3

# create a flask application and assign to app variable
app = Flask(__name__)

# creates app configuration based on our config class
app.config.from_object(Config)

# set debugging to True to show errors on the screen, rather than Bad Gateway message
app.config["DEBUG"] = True

# set static assets folder
app.static_folder = 'static'

from app import routes
