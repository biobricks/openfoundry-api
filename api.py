###
import flask
from flask import request, jsonify
import sqlite3

# create a flask application and assign to app variable
app = flask.Flask(__name__)

# set debugging to True to show errors on the screen, rather than Bad Gateway message
app.config["DEBUG"] = True

# Example Virtuals Data
# ToDo: Replace with SQLite DB

virtuals = [
  {'id': 0,
   'name': 'Foo',
   'description': 'It\'s a Foo.'},
  {'id': 1,
   'name': 'Bar',
   'description': 'It\'s a Bar.'},
  {'id': 2,
   'name': 'Baz',
   'description': 'This is a Baz.'},
  {'id': 3,
   'name': 'Quay',
   'description': 'A Quay.'},   
]



##########
# routes #
##########
# all assume extension to a domain name / IP address / localhost
# example: 
# '/' = openfoundry.xyz
# '/about' = openfoundry.xyz/about


################
# landing page #
################
# openfoundry.xyz
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome To The OpenFoundry API</h1>"

# ex. openfoundry.xyz/api/v1/resources/virtuals/all
@app.route('/api/v1/resources/virtuals/all', methods=['GET'])
def virtuals_all():
  return jsonify(virtuals)



##################################
# get virtual by id with filters #
##################################
# openfoundry.xyz/api/v1/resources/virtuals?id=0
@app.route('/api/v1/resources/virtuals', methods=['GET'])
def virtual_id():
  # assign the request args (id, name) to a variable
  query_parameters = request.args

  # attempt to retrieve ?id=
  id = query_parameters.get('id')
  # attempt to retrieve ?name=
  name = query_parameters.get('name')
  # attempt to retrieve ?description=
  description = query_parameters.get('description')

  filters = []

  # if id exists
  if id:
    # add id to filters
    filters.append({"id": id})
  # if name exists
  if name:
    # add name to filters
    filters.append({"name": name})  
  # if description exists
  if description:
    # add description to filters
    filters.append({"description": description}) 


  # empty list to hold the results
  results = []

  # iterate each filter
  for filter in filters:
    # iterate each filter's key/value pairs
    for filter_key, filter_value in filter.items():          
      # iterate each virtual
      for virtual in virtuals:
        # iterate each virtuals key/value pairs                               
        for virtual_key, virtual_value in virtual.items():
          # if virtual key does not equal 'description'
          # do exact matching
          if str(virtual_key) != "description":
            # if virtual key equals filter key and 
            # if the virtual value equals filter value
            # required wrapping variables in string object, str(), in order for the comparison to work
            if str(virtual_key) == str(filter_key) and str(virtual_value) == str(filter_value): 
              # add virtual to results
              results.append(virtual)
          # else if the virtual key equals description
          # look for results to contain the description query
          else:
            # if the virtual key is equal to the filter key and
            # if the virtual value contains at least one instance of the filter value
            if str(virtual_key) == str(filter_key) and str(virtual_value).find(str(filter_value)) > -1:
              # add virtual to results
              results.append(virtual)              

  
  # return the results in json
  return jsonify(results)



###########################
# not found error handler #
###########################
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run() 