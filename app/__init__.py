from flask import Flask

import sqlite3

# create a flask application and assign to app variable
app = Flask(__name__)

# set debugging to True to show errors on the screen, rather than Bad Gateway message
app.config["DEBUG"] = True

from app import routes
