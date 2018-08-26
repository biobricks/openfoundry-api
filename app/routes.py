from app import app, db
from flask import request, jsonify, render_template, flash, redirect, url_for
from app.forms import LoginForm, SignupForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

# Example Virtuals Data
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


# openfoundry.xyz
@app.route('/', methods=['GET'])
def index():
  title = "Welcome"
  return render_template('index.html', title=title)

# openfoundry.xyz/login
@app.route('/login', methods=['GET', 'POST'])
def login():
  title = "Login"
  # validate 1. if there is a user logged in
  if current_user.is_authenticated:
    # redirect to the index page
    return redirect(url_for('index'))
  # form set to instantiate /app/forms/LoginForm 
  form = LoginForm()
  # if there is a POST with form data
  if form.validate_on_submit():
    # db query for user by the username form field
    user = User.query.filter_by(username=form.username.data).first()
    # validate 2. if there is no user found in db or the password check fails
    if user is None or not user.check_password(form.password.data):
      # set flash messsage
      flash('Incorrect Username or Password')
      # login failed - redirect to the current page showing the alert
      return redirect(url_for('login'))
    
    # login has passed validation - log user in with optional remember me
    login_user(user, remember=form.remember_me.data)
    
    # friendly redirect - requiring login redirects to login page, 
    # successful login redirects to user's original intended location
    
    # get the next argument from the login url
    next_page = request.args.get('next')
    # if there is no next argument or 
    # the next argument is set to a absolute path rather than a relative one
    # absolute path for next is an attack vector, we want relative only 
    if not next_page or url_parse(next_page).netloc != '':
      # set the next page argument to the index page
      next_page = url_for('index')
    
    # redirect to the route specified by the next_page variable
    return redirect(next_page)
  # if there is a GET request to the route, render the form  
  return render_template('login.html', title=title, form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  title = "Signup"
  # validate 1. if there is a user logged in
  if current_user.is_authenticated:
    # redirect to the index page
    return redirect(url_for('index'))  
  # form set to instantiate /app/forms/SignupForm 
  form = SignupForm()
  # if there is a POST with form data
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    password = user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Your new account was successfully created. Please login.')
    return redirect(url_for('login'))
  return render_template('signup.html', title=title, form=form)  

# user profile
@app.route('/users/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('user.html', user=user)






# openfoundry.xyz/api/v1/documentation
@app.route('/api/v1/documentation', methods=['GET'])
def documentation_version_one():
  title = "API Version 1 - Documentation"
  return render_template('docs_v1.html', title=title)

# openfoundry.xyz/api/v1/resources/virtuals/all
@app.route('/api/v1/resources/virtuals/all', methods=['GET'])
def virtuals_all():
  return jsonify(virtuals)

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

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404