# runs /app/__init__.py by default
# imports database
from app import app, db

# get models to load into flask shell
from app.models import User, Comment

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Comment': Comment}