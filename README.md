# OpenFoundry API

## Environment Variables
The application is configured using environment variables found in .env files. To use these files, install the [python-dotenv](https://github.com/theskumar/python-dotenv) module:
```
pip install python-dotenv --user
```

### .flaskenv
This is the configuration for the flask application environment.

#### FLASK_APP
default: /opefoundry.py  
description: The entry point script to be executed on ```flask run```.

#### FLASK_ENV
default: development  
description: The server environment. Development enables the debugging console.

## Run
```
flask run
```