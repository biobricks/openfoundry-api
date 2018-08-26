from datetime import datetime
from app import db

# the user class inherits from db.Model, a base class for all models from flask-SQLAlchemy
class User(db.Model):
    # fields are created as instances of db.Column class and take arg of field type plus optional args
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # __repr__ method tells python how to print the class
    def __repr__(self):
        return '<User {}>'.format(self.username)

# the comment class - to show db relationship to user with foreign key
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Comment {}>'.format(self.body)