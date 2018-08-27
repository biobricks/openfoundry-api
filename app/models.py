from hashlib import md5
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# the user class inherits from:
#  UserMixin, a class that adds the necessary fields for flask-login
#  db.Model, a base class for all models from flask-SQLAlchemy
class User(UserMixin, db.Model):
    # fields are created as instances of db.Column class and take arg of field type plus optional args
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bio = db.Column(db.String(140))
    last_online = db.Column(db.DateTime, default=datetime.utcnow)
    # __repr__ method tells python how to print the class
    def __repr__(self):
      return '<User {}>'.format(self.username)

    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)

    def avatar(self, size):
      digest = md5(self.email.lower().encode('utf-8')).hexdigest()
      return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size) 

# the comment class - to show db relationship to user with foreign key
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Comment {}>'.format(self.body)

class Virtual(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, unique=True)
  genbank_file = db.Column(db.String(10000000))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  

  def __repr__(self):
    return '<Virtual {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))    