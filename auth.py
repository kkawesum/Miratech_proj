import jwt
import os
from flask import Flask, request, jsonify, make_response, render_template, abort
import datetime
from snowflake_conn import conn
import base64
from aws_conn import check_file
from ingestion import ingest_sf

app = Flask(__name__)
# secret key for encoding 
app.config['secret_key'] = "this is secret"
file_searched=''

def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


def token_required(f):
	'''
	Function that checks whether we already have a JWT token assigned
	'''
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		if not token:
			return jsonify({'error': 'token is missing'}), 403
		try:
			jwt.decode(token, app.config['secret_key'], algorithms="HS256")
		except Exception as error:
			return jsonify({'error': 'token is invalid/expired'})
		return f(*args, **kwargs)
	return decorated

@app.route("/search")
def search():
	'''
	Search for a particular file in the back-end 
	'''

	return render_template("search.html")

@app.route('/read-form', methods=['POST']) 
def read_form(): 
    '''
	Read the values in the Search form to get the filename
	'''

    # Get the form data as Python ImmutableDict datatype  
    data = request.form 
    file_name = data['username']
    ## Return the extracted information
    return f'<a href="http://localhost:5000/get_file?{file_name}">Private link</a>'


'''Endpoint for fetching the required file from the back-end storage'''
@app.route("/get_file/{file_name}")
def get_file(file_name):
	global file_searched
	file_searched = file_name
	if(check_file(file_name=file_name)):
		ingest_sf(file_name)
	return base64.urlsafe_b64encode(os.urandom(32))

'''The default homepage'''
@app.route('/')
def index():
	return render_template("home.html")

'''Authentication endpoint - logging in a created user'''
@app.route("/login")
def login():
	auth = request.authorization
	if auth and auth.password == "password":
		token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
		) + datetime.timedelta(seconds=10)}, app.config['secret_key'])
		return f'<a href="http://localhost:5000/access?token={token}">Private link</a>'
	return make_response('Could not Verify', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})

'''Endpoint for invoking the Search service when the user has been authenticated using a token'''
@app.route("/access")
@token_required
def access():

	return f'<a href="http://localhost:5000/search">Go to Search Service</a>'

if __name__ == "__main__":
	app.run()
