# OpenFoundry API

## CLI

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
