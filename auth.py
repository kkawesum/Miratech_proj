import jwt
from flask import Flask, request, jsonify, make_response, render_template
import datetime

app = Flask(__name__)

app.config['secret_key'] = "this is secret"


def token_required(f):
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
    return render_template("search.html")

@app.route('/read-form', methods=['POST']) 
def read_form(): 
  
    # Get the form data as Python ImmutableDict datatype  
    data = request.form 
    file_name = data['username']
    ## Return the extracted information
    return f'<a href="http://localhost:5000/get_file?{file_name}">Private link</a>'


    
@app.route("/login")
def login():
	auth = request.authorization
	if auth and auth.password == "password":
		token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
		) + datetime.timedelta(seconds=10)}, app.config['secret_key'])
		return f'<a href="http://localhost:5000/access?token={token}">Private link</a>'
	return make_response('Could not Verify', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})


@app.route("/access")
@token_required
def access():

	return f'<a href="http://localhost:5000/search">Go to Search Service</a>'

if __name__ == "__main__":
	app.run()
