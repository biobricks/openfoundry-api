# OpenFoundry API

## Requirements

### Python
[Python Download Page](https://www.python.org/downloads/)

### Pip
[Pip Download Page](https://pip.pypa.io/en/stable/installing/)

### Virtualenv
[Virtualenv Download Page](https://virtualenv.pypa.io/en/stable/installation/)



## Installation

### Clone
```
git clone https://github.com/biobricks/openfoundry-api.git
cd openfoundry-api
```

### Create Virtual Environment
```
virtualenv venv
```

### Active Virtual Instance

#### Linux/Unix
```
source venv/bin/activate
```

#### Windows
```
venv\Scripts\activate
```

#### Install Dependencies
```
pip install flask python-dotenv flask-wtf flask-sqlalchemy flask-migrate
```






## Configuration

### Flask Environment Variables
The flask environment is configured using variables found in .env files. To use these files, install the [python-dotenv](https://github.com/theskumar/python-dotenv) module:
```
pip install python-dotenv --user
```

### .flaskenv
This is the configuration for the flask application environment.

##### FLASK_APP
default: /openfoundry.py  
description: The entry point script to be executed on ```flask run```.

##### FLASK_ENV
default: development  
description: The server environment. Development enables the debugging console.

### Application Configuration
The application configuration is loaded from a class found at [config.py](https://github.com/biobricks/openfoundry-api/blob/master/config.py).


## Flask CLI

## Create Database Migration Repository
```
flask db init
```

## Create Database Migration
```
flask db migrate -m "my migration message"
```

## Run Database Migration/s
```
flask db upgrade
```

## Undo Last Database Migration
```
flask db downgrade
```

## Run Application
```
flask run
```

## Development

### Creating New Database Model
Example: Comment Class

#### Add Model
Add model to [models.py](https://github.com/biobricks/openfoundry-api/blob/master/app/models.py):
```python
from datetime import datetime
from app import db

# other classes

class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey(user.id))

  def __repr__(self):
    return '<Comment {}>'.format(self.body)
```

#### Generate Migration
Since we changed our database models, we changed our database structure and need to generate a migration. We added a comments table, that will be our migration message:
```
flask db migrate -m "comments table"
```

#### Run Migration On Database
Generating a migration does not alter the database. We have to run the migration:
```
flask db upgrade
```